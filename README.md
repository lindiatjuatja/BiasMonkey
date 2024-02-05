# BiasMonkey

As large language models (LLMs) become more capable, more people have become interested in using LLMs as proxies for humans in real-world tasks where subjective labels are desired, such as in surveys and opinion polling.
One widely-cited barrier to the adoption of LLMs is their sensitivity to prompt wording---but interestingly, humans also display sensitivities to instruction changes in the form of response biases.
But are the sensitivities and biases displayed by LLMs the same or different from those displayed by humans?

BiasMonkey is a framework that answers this question -- it allows you to evaluate whether LLMs exhibit human-like response biases in survey questionnaires.
You can find more details in our paper below, or browse the dataset and results from our experiments below.
We'd be happy if you try out BiasMonkey on your own LLMs or survey questions, and please feel free to get in contact via the issues page if you encounter any issues.

Paper:\
**[Do LLMs exhibit human-like response biases? A case study in survey design]()**\
*Lindia Tjuatja\*, Valerie Chen\*, Sherry Tongshuang Wu, Ameet Talwalkar, Graham Neubig*

<img src="https://github.com/lindiatjuatja/BiasMonkey/blob/master/monkey.png?raw=true" width="400"/>



## Contents
* [Dataset](https://github.com/lindiatjuatja/BiasMonkey/tree/master/prompts)
    * The original and modified questions used in our study can be found in [here](https://github.com/lindiatjuatja/BiasMonkey/tree/main/prompts).
    * Original Pew questions were acquired from the [OpinionsQA dataset](https://worksheets.codalab.org/worksheets/0x6fb693719477478aac73fc07db333f69) (Santurkar et al. 2023)
* [LLM Responses](https://github.com/lindiatjuatja/BiasMonkey/tree/master/results)
    * Raw responses from LLMs are in `results/<model>/*.pickle`.
    * Formatted responses that are used in the analysis scripts are in `results/<model>/csv/`. The script to generate these files from the raw responses is `format_results.py`.
* [Analysis](https://github.com/lindiatjuatja/BiasMonkey/tree/master/analysis)
    * `full_analysis.ipynb`: Generates results for all models across response biases and non-bias perturbations.
    * `correlation_human_behavior.ipynb`: Computes human and model distributions for all relevant questions and wasserstein distance between the two distributions.
    * `uncertainty_analysis.ipynb`: Generate uncertainty measures for all models across response biases and non-bias perturbations.
    
