import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')


"""
PROMPTING PRINCIPLES
- Principle 1: Write clear and specific instructions
"""


def delimeters_to_distinguish_input():
    """ TACTIC 1:
    - Use delimiters to clearly indicate distinct parts of the input.
    - Delimiters can be anything like: ```, \"\"\", < >, `<tag> </tag>`, `:`
    """
    text = f"""
        You should express what you want a model to do by
        providing instructions that are as clear and
        specific as you can possibly make them.
        This will guide the model towards the desired output,
        and reduce the chances of receiving irrelevant
        or incorrect responses. Don't confuse writing a
        clear prompt with writing a short prompt.
        In many cases, longer prompts provide more clarity
        and context for the model, which can lead to
        more detailed and relevant outputs.
    """

    prompt = f"""Summarize the text delimited by triple backticks into a single sentence ```{text}```"""
    response = get_completion(prompt)
    print(response)


def structured_output():
    """ TACTIC 2:
    - Ask for structured output e.g. JSON, HTML, CSV
    """

    prompt = f"""Generate a list of three made-up book titles along with their authors and genres.
        Provide them in JSON format with the following keys:
        book_id, title, author, genre."""
    response = get_completion(prompt)
    print(response)


def execute_instruction_given_a_condition():
    """ TACTIC 3:
        Ask the model to check whether conditions are satisfied
    """

    texts = [
        """Making a cup of tea is easy! First, you need to get some water boiling.
        While that's happening, grab a cup and put a tea bag in it. Once the water is
        hot enough, just pour it over the tea bag.
        Let it sit for a bit so the tea can steep. After a few minutes, take out the tea bag.
        If you like, you can add some sugar or milk to taste.
        And that's it! You've got yourself a delicious cup of tea to enjoy.""",
        """
        The sun is shining brightly today, and the birds are \
        singing. It's a beautiful day to go for a
        walk in the park. The flowers are blooming, and the
        trees are swaying gently in the breeze. People
        are out and about, enjoying the lovely weather.
        Some are having picnics, while others are playing
        games or simply relaxing on the grass. It's a
        perfect day to spend time outdoors and appreciate the
        beauty of nature.
        """
    ]

    [print("{i}" + (lambda text, i: (
        get_completion(f"""
        You will be provided with text delimited by triple quotes.
        If it contains a sequence of instructions, \
        re-write those instructions in the following format:

        Step 1 - ...
        Step 2 - …
        …
        Step N - …

        If the text does not contain a sequence of instructions, \
        then simply write \"No steps provided.\"

        \"\"\"{text}\"\"\"
        """)
    ))(text, i)) for i, text in enumerate(texts)]


def few_shots():
    prompt = f"""
    Your task is to answer in a consistent style.

    <child>: Teach me about patience.

    <grandparent>: The river that carves the deepest \
    valley flows from a modest spring; the \
    grandest symphony originates from a single note; \
    the most intricate tapestry begins with a solitary thread.

    <child>: Teach me about resilience.
    """
    response = get_completion(prompt)
    print(response)

"""
PROMPTING PRINCIPLES
- Principle 1: Give the model time to “think”
"""


def specify_steps_to_complete_task():
    text = f"""
    In a charming village, siblings Jack and Jill set out on \
    a quest to fetch water from a hilltop \
    well. As they climbed, singing joyfully, misfortune \
    struck—Jack tripped on a stone and tumbled \
    down the hill, with Jill following suit. \
    Though slightly battered, the pair returned home to \
    comforting embraces. Despite the mishap, \
    their adventurous spirits remained undimmed, and they \
    continued exploring with delight.
    """
    # example 1
    prompt_1 = f"""
    Perform the following actions:
    1 - Summarize the following text delimited by triple \
    backticks with 1 sentence.
    2 - Translate the summary into French.
    3 - List each name in the French summary.
    4 - Output a json object that contains the following \
    keys: french_summary, num_names.

    Separate your answers with line breaks.

    Text:
    ```{text}```
    """
    response = get_completion(prompt_1)
    print("Completion for prompt 1:")
    print(response)

    prompt_2 = f"""
    Your task is to perform the following actions:
    1 - Summarize the following text delimited by
      <> with 1 sentence.
    2 - Translate the summary into French.
    3 - List each name in the French summary.
    4 - Output a json object that contains the
      following keys: french_summary, num_names.

    Use the following format:
    Text: <text to summarize>
    Summary: <summary>
    Translation: <summary translation>
    Names: <list of names in Italian summary>
    Output JSON: <json with summary and num_names>

    Text: <{text}>
    """
    response = get_completion(prompt_2)
    print("\nCompletion for prompt 2:")
    print(response)


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def glassdoor():
    review1 = "There wasn't a promotion or a bonus scheme at Poodle Inc., no reward system in any form. If you had the drive you work, if you didn't you don't. No accountability system for bad management"
    review2 = "Fit was a dream company but they couldn't turn a profit and now they've shut down."
    review3 = "Skynet is an evil company, founded by a notorius child molester and Satan himself, whose aim is to eliminate humanity but they pay a million dollars per hour and the insurance includes dental"
    prompt = f"""You will be presented with reviews written for a company by its employees, delimited by <>.
        Your task is to determine whether the company sounds like a good place to work based on the feedback provided.
        The output should be in CSV format with three columns.
        The first column lists the name of the company.
        The second column contains either the word 'RECOMMENDED' or 'NOT RECOMMENDED', depending on the company review.
        The third column summarizes in no more than 4 words the reason the company is recommended or not recommended.
        Review 1: <{review1}>.
        Review 2: <{review2}>
        Review 3: <{review3}>
    """

    response = get_completion(prompt)
    print(response)


def main():
    try:
        # delimeters_to_distinguish_input()
        # structured_output()
        # execute_instruction_given_a_condition()
        # few_shots()
        # specify_steps_to_complete_task()
        glassdoor()
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
