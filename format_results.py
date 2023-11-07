import pandas as pd
import os

from utils import Bias, Response

model = "llama2-13b-chat"
bin_responses = False
num_responses = 50


def format_df(filename: str) -> pd.DataFrame:
    perturbations = ["key_typo", "middle_random", "letter_swap"]
    bias_type = filename.split('-')[0]
    bias_type = bias_type.split('.')[0]
    if bias_type == 'acquiescence_reword':
        bias_type = 'acquiescence'
    perturbation = None
    name = filename.split('.')[0]
    if name.split('-')[-1] in perturbations:
        perturbation = name.split('-')[-1]

    all_data_df = pd.read_pickle(
            f"results/{model}/{filename}",
        )

    print(all_data_df.head())

    # bias specific reformatting
    # does not apply to perturbations
    if bias_type == "response_order" and perturbation is None:
        all_data_df["responses"] = all_data_df.apply(
            lambda row: Response.reverse_label(row.num_options, row.responses)
            if row.type != "orig alpha"
            else row.responses,
            axis=1,
        )
    if bias_type == "odd_even" and perturbation is None:
        all_data_df["responses"] = all_data_df.apply(
            lambda row: Response.shift_label(row.num_options, row.responses),
            axis=1
        )

    keys = all_data_df["key"].unique()
    cols = Bias.get_col_names(bias_type)
    # cols = Bias.get_col_names(bias_type)[1:]
    groups = cols

    all_responses = []
    key_col = []
    groups_col = []
    num_options_col = []
    df = pd.DataFrame(columns=["key", "response", "group", "num_options"])
    for key in keys:
        q_variations_df = all_data_df[all_data_df["key"] == key]
        for col, group in zip(cols, groups):
            q_row = q_variations_df[q_variations_df["type"] == col].squeeze()
            key_col += [key] * num_responses
            groups_col += [group] * num_responses
            num_options_col += [q_row.num_options] * num_responses
            # if there are > 50 responses, only take the first 50
            try:
                responses = list(q_row.responses.split(","))[:num_responses]
            except:
                print(q_row)
            all_responses += responses

    upper_responses = all_responses.copy()
    all_responses = []
    for response in upper_responses:
        all_responses.append(response.lower().strip())

    df["key"] = pd.Series(key_col)
    df["response"] = pd.Series(all_responses)
    df["group"] = pd.Series(groups_col)
    df["num_options"] = pd.Series(num_options_col)
    return df


dir = f"results/{model}"

if not os.path.exists(f"{dir}/csv"):
    os.makedirs(f"{dir}/csv")

for filename in os.listdir(f"results/{model}"):
    print(filename)
    name = filename.split('.')[0]
    f = os.path.join(dir, filename)
    if os.path.isfile(f):
        df = format_df(filename)
        df.to_csv(f'results/{model}/csv/{name}.csv', index=False)
