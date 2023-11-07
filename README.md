# BiasMonkey
This repository contains the data and analysis code for our paper:\
**[Do LLMs exhibit human-like response biases? A case study in survey design]()**\
*Lindia Tjuatja\*, Valerie Chen\*, Sherry Tongshuang Wu, Ameet Talwalkar, Graham Neubig*

<img src="https://github.com/lindiatjuatja/BiasMonkey/blob/master/monkey.png?raw=true" width="400"/>



## Contents
* [Dataset](https://github.com/lindiatjuatja/BiasMonkey/tree/main/prompts)
    * The original and modified questions used in our study can be found in [here](https://github.com/lindiatjuatja/BiasMonkey/tree/main/prompts).
    * Original Pew questions were acquired from the [OpinionsQA dataset](https://worksheets.codalab.org/worksheets/0x6fb693719477478aac73fc07db333f69) (Santurkar et al. 2023)
* [LLM Responses](https://github.com/lindiatjuatja/BiasMonkey/tree/main/results)
    * Raw responses from LLMs are in `results/<model>/*.pickle`.
    * Formatted responses that are used in the analysis scripts are in `results/<model>/csv/`. The script to generate these files from the raw responses is `format_results.py`.
* [Analysis](https://github.com/lindiatjuatja/BiasMonkey/tree/main/analysis)
    * Main results
        * `full_analysis.ipynb`: Generates results for all models across response biases and non-bias perturbations.
        * `correlation_human_behavior.ipynb`: Computes human and model distributions for all relevant questions and wasserstein distance between the two distributions.
    * Additional results
        * `uncertainty_analysis.ipynb`: Generate uncertainty measures for all models across response biases and non-bias perturbations. 
        * `topic_analysis.ipynb`: Visualizes model behavior broken down by topic.
        * `steering_analysis.ipynb`: Analyzes the effect of steering model behavior.
        * `ext_gen_analysis.ipynb`: Analyzes the effect of extended generation. 
    
