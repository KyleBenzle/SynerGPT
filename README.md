# SynerGPT

SynerGPT is an innovative project that enables collaboration between two Large Language Models (LLMs) to efficiently solve complex problems and tackle extensive tasks. By harnessing the power of Anthropic's and OpenAI's LLMs, SynerGPT creates a synergistic environment where a Manager LLM assigns tasks to a Worker LLM, fostering seamless communication and cooperation.
<p align="center"> <center>

![SynerGPT](https://github.com/KyleBenzle/SynerGPT/assets/48848725/cef04e52-c633-4ee6-bfd6-521fc0452342)
</center>
</p>
## Overview

In SynerGPT, the Anthropic LLM assumes the role of the Manager, overseeing the project and delegating tasks to the Worker LLM, which is powered by OpenAI. The Manager LLM breaks down large jobs into smaller, manageable tasks and assigns them to the Worker LLM. This collaborative approach allows for efficient problem-solving and task completion.

The communication between the Manager and Worker LLMs is facilitated by a Python script called `Control.py`. This script acts as a mediator, controlling the flow of information and ensuring smooth interaction between the LLMs. All prompts and responses exchanged during the collaboration are recorded in a `ChatLog.txt` file, providing a comprehensive record of the project's progress.

## Key Features

- **Dual LLM Collaboration**: SynerGPT leverages the combined capabilities of Anthropic's and OpenAI's LLMs to tackle complex problems effectively.
- **Manager-Worker Paradigm**: The Manager LLM assigns tasks to the Worker LLM, ensuring efficient task allocation and completion.
- **Seamless Communication**: The `Control.py` script facilitates smooth communication between the Manager and Worker LLMs.
- **Comprehensive Logging**: All prompts and responses are recorded in the `ChatLog.txt` file, providing a detailed history of the project's progress.
- **Scalability**: SynerGPT is designed to handle large-scale tasks by breaking them down into smaller, manageable subtasks.


# Full Description

SynerGPT is an innovative project that showcases the power of collaboration between two Large Language Models (LLMs) to solve complex problems and tackle extensive tasks efficiently. By leveraging the capabilities of Anthropic's and OpenAI's LLMs, SynerGPT creates a synergistic environment where a Manager LLM assigns tasks to a Worker LLM, fostering seamless communication and cooperation.

The primary objective of SynerGPT is to demonstrate how LLMs can work together in a structured manner to break down large jobs into smaller, manageable tasks. The Manager LLM takes on a supervisory role, overseeing the project and delegating tasks to the Worker LLM. This collaborative approach allows for efficient problem-solving and task completion, even for complex and time-consuming projects.

SynerGPT utilizes a Python script called `Control.py` to facilitate communication between the Manager and Worker LLMs. This script acts as a mediator, controlling the flow of information and ensuring smooth interaction between the LLMs. All prompts and responses exchanged during the collaboration are recorded in a `ChatLog.txt` file, providing a comprehensive record of the project's progress.

One of the key features of SynerGPT is its scalability. The project is designed to handle large-scale tasks by breaking them down into smaller, manageable subtasks. This approach enables the LLMs to tackle complex problems more effectively and efficiently.

SynerGPT serves as a proof of concept for the potential of LLM collaboration in various domains, such as natural language processing, problem-solving, and task automation. By showcasing the synergy between different LLMs, SynerGPT opens up new possibilities for leveraging the strengths of multiple language models to achieve greater efficiency and accuracy in task completion.

Whether you are a researcher, developer, or enthusiast interested in exploring the capabilities of LLMs, SynerGPT provides a framework for experimenting with collaborative problem-solving using language models. The project's modular design and well-documented codebase make it easy to extend and adapt to specific use cases.

We invite you to explore SynerGPT, contribute to its development, and witness the power of LLM collaboration in action. Join us in pushing the boundaries of what LLMs can achieve when working together seamlessly.

## Getting Started

To get started with SynerGPT, follow these steps:

1. Clone the repository.
2. Install the required dependencies.
3. Set up the necessary API keys for Anthropic and OpenAI in the respective LLM scripts.
4. Run the `Control.py` script to initiate the collaboration between the Manager and Worker LLMs.
5. Provide the initial prompt and specify the number of collaboration cycles.
6. Monitor the progress and view the results in the `ChatLog.txt` file.

## Contributing

We welcome contributions to enhance SynerGPT and expand its capabilities. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
