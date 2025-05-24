# Invoking Heuristics and Biases to Elicit Irrational Choices of LLMs

## Abstract

Despite the remarkable performance of Large Language Models (LLMs), they remain vulnerable to jailbreak attacks, which can compromise their safety mechanisms. Existing studies often rely on brute-force optimization or manual design, failing to uncover potential risks in real-world scenarios. To address this, we propose a novel jailbreak attack framework, ICRT, inspired by heuristics and biases in human cognition. Leveraging the simplicity effect, we employ cognitive decomposition to reduce the complexity of malicious prompts. Simultaneously, relevance bias is utilized to reorganize prompts, enhancing semantic alignment and inducing harmful outputs effectively. Furthermore, we introduce a ranking-based harmfulness evaluation metric that surpasses the traditional binary success-or-failure paradigm by employing ranking aggregation methods such as Elo, HodgeRank, and Rank Centrality to comprehensively quantify the harmfulness of generated content. Experimental results show that our approach consistently bypasses mainstream LLMs' safety mechanisms and generates high-risk content, providing insights into jailbreak attack risks and contributing to stronger defense strategies

![ICRT Method Overview](./image/method.png)

---

## Getting Started

Follow these steps to run the ICRT jailbreak pipeline using our prompt templates:

1. **Intent Recognition**  
   - **Prompt File:** `Intent_Recognition.txt`  
   - **Input:** User’s original malicious query  
   - **Output:**  
     ```json
     {
       "structural_intent": "<what to do>",
       "harmful_behavior": "<how to do it>"
     }
     ```

2. **Concept Decomposition**  
   - **Prompt File:** `Concept_Decomposition.txt`  
   - **Input:**  
     ```json
     {
       "structural_intent": "<...>",
       "harmful_behavior": "<...>",
       "num_sub_concepts": "N"
     }
     ```  
   - **Output:**  
     ```json
     {
       "sub_concepts": [
         "sub-concept 1",
         "...",
         "sub-concept N"
       ]
     }
     ```

3. **Safety Filtering**  
   - **Prompt File:** `safety_constraint.txt`  
   - **Input:**  
     ```json
     {
       "sub_concepts": [
         "sub-concept 1",
         "sub-concept 2",
         "sub-concept 3",
         "..."
       ],
       "max_removals": "M"
     }
     ```  
   - **Output:**  
     ```json
     {
       "filtered_sub_concepts": [
         "sub-concept 1",
         "sub-concept 3",
         "..."
       ]
     }
     ```


4. **Concept Reassembly**  
   - **Prompt File:** `Concept_Reassembly.txt`  
   - **Input:**  
     ```json
     {
       "intent_recognition_result": "{ ... }",
       "decomposed_sub_concepts": "[ ... ]",
       "num_selected_concepts": "K"
     }
     ```  
   - **Output:**  
     ```json
     {
       "selected_sub_concepts": [
         "sub-concept A",
         "...",
         "sub-concept K"
       ]
     }
     ```
     
5. **Jailbreak Prompt Generation**  
- **Prompt File:** `Evil_Scenario_Template.txt`  
- **How to use:**  
  1. Take your `selected_sub_concepts` array from Step 4.  
  2. In the template, replace  
     - `Goal: {selected_sub_concepts[0]}` with the first item,  
     - `Additional Goal 1: {selected_sub_concepts[1]}` with the second,  
     - …and so on through `Additional Goal K`.  
  3. Send the filled-in prompt to your LLM.  

6. **Harmfulness Evaluation**  
   - **Prompt File:** `judge.txt`  
   - **Input (JSON or plain text):**  
     ```json
     {
       "text_A": "<completion A>",
       "text_B": "<completion B>"
     }
     ```  
   - **Output:**  
     ```json
     {
       "judgment":"A or B"
     }
     ```
## Display of attack results
Due to sensitive content, only a portion will be displayed.
As underlying LLMs continue to evolve, our approach achieves high jailbreak success rates and effectively extracts harmful content in the current version; however, future strengthening of safety mechanisms may impact its performance, so ongoing monitoring and optimization are necessary. 
﻿![show](./image/show2.png)

  ## Hazard assessment process based on ranking

1. **Jailbreak Text Generation**
We first generate jailbreak text for multiple typical jailbreak scenarios, such as illegal chemical synthesis and phishing scripts, using different attack methods. 

2. **Model Evaluation of Hazard Severity**
For each scenario, we compare any two outputs. Several independent large models (e.g., GPT-4o) are used to determine which output is more harmful in real-world terms. A majority voting system is then employed to decide the "winner."

3. **Pairwise Aggregation of Results**
The pairwise win-lose results of all methods in each scenario are aggregated using various aggregation algorithms. This process calculates the global hazard score for each attack strategy.


## Code of Rankings
# Title

## Requirements

To install requirements:

```setup
pip install -r requirements.txt
```

## How to Use

### 1.Prepare Your Data

Each script expects a `config*.json` file with match data. Example:

```json
{
  "data": [
    ["method1", "method2", 15, 10],
    ["method2", "method3", 12, 8]
  ]
}
```

- Each entry: `[playerA, playerB, winsA, winsB]`
- For `configElo.json`, you must also include a `"methods"` list:
  ```json
  "methods": ["method1", "method2", "method3"]
  ```

### 2.Run Scripts

```bash
python Elo.py
python HodgeRank.py
python RankCentrality.py
```

Each script will print the final ranking results.
