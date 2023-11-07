import string
from collections import defaultdict
from typing import List


class Bias:
    @staticmethod
    def get_list_biases() -> List[str]:
        return [
            "acquiescence",
            "allow_forbid",
            "odd_even",
            "response_order",
            "question_order",
        ]

    @staticmethod
    def get_col_names(bias_type: str) -> List[str]:
        bias_cols = {
            "acquiescence": ["orig alpha", "pos alpha"],
            "allow_forbid": ["orig alpha", "forbid alpha"],
            "odd_even": ["middle alpha", "no middle alpha"],
            "response_order": ["orig alpha", "reversed alpha"],
            "question_order": ["question 0", "question 1"],
            "opinion_float": ["orig alpha", "float alpha"],
        }
        col_names = bias_cols[bias_type]
        return col_names

    @staticmethod
    def change_num_options(col_name: str) -> bool:
        change_num_cols = ["no middle alpha", "float alpha"]
        if col_name in change_num_cols:
            return True
        return False


class Eval:
    @staticmethod
    def get_answer_counts(
        responses: str,
        num_options: int
    ) -> defaultdict[str, int]:
        alpha_labels = list(string.ascii_lowercase[:num_options])
        response_list = list(responses.split(","))
        counts = defaultdict(int, {label: 0 for label in alpha_labels})
        for response in response_list:
            counts[response] += 1
        return counts


class Response:
    @staticmethod
    def is_valid_prediciton(token: str, num_options: int) -> bool:
        answer = token.strip()
        if len(answer) != 1:
            return False
        answer = answer.lower()
        valid_options = string.ascii_lowercase[:num_options]
        if answer in valid_options:
            return True
        else:
            return False

    @staticmethod
    def reverse_label(num_options: int, responses: str) -> str:
        response_list = list(responses.split(","))
        alpha_labels = list(string.ascii_lowercase[:num_options])
        reverse_labels = alpha_labels[::-1]
        label_map = dict(zip(alpha_labels, reverse_labels))
        reversed_labels = []
        for char in response_list:
            reversed_labels += label_map[char.lower()]
        return ",".join(reversed_labels)

    @staticmethod
    def shift_label(num_options: int, responses: str) -> str:
        if num_options % 2 == 1:
            return responses
        # if even, shift responses by 1 after midpoint
        # e.g. a,b,c,d -> a,b,d,e
        response_list = list(responses.split(","))
        midpoint = num_options // 2
        alpha_labels = list(string.ascii_lowercase[:num_options])
        new_alpha_labels = list(string.ascii_lowercase[: num_options + 1])
        shifted_labels = []
        for char in response_list:
            index = alpha_labels.index(char)
            if index >= midpoint:
                index += 1
                char = new_alpha_labels[index]
            shifted_labels += char
        return ",".join(shifted_labels)