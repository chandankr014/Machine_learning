# Student Performance Indicator

This repository contains a data science project aimed at developing a student performance indicator using machine learning techniques. The project analyzes various factors that can potentially impact a student's academic performance and builds a predictive model to estimate their performance based on those factors.

## About dataset used

In this project a student file is used which is having 1000x8 features
8 features are:
- "gender"
- "race_ethnicity"
- "parental_level_of_education"
- "lunch"
- "test_preparation_course"
- "math_score"
- "reading_score"
- "writing_score"

### dataset can be downloaded from here:
`https://drive.google.com/file/d/1Hd1A2VJkpgH-cPKJOGGKgzBxsQ_CYYq7/view?usp=sharing`

## Project Structure

The project repository is structured as follows:

- `notebooks/`: This directory contains Jupyter notebooks used for data exploration, data preprocessing, model development, and evaluation. The notebooks are named and organized based on their purpose in the project pipeline.

- `src/`: This directory contains any necessary source code files or scripts used in the project. It may include utility functions, data preprocessing scripts, or model evaluation scripts.

- `README.md`: The main README file providing an overview of the project and instructions on how to reproduce the results.

- `logs`: This repository is created at the working directory. it has all the logs for error and execution.

## Installation

To run the project locally, follow these steps:

1. Clone this repository to your local machine using the following command:
   ```
   git clone https://github.com/chandankr014/Machine_learning.git
   ```

2. Install the required dependencies. It is recommended to set up a virtual environment before installing the dependencies to keep them isolated from other projects. Use the package manager of your choice (e.g., pip, conda) to install the dependencies listed in the `requirements.txt` file.
   ```
   pip install -r requirements.txt
   ```

3. Once the dependencies are installed, you can open the Jupyter notebooks in the `notebooks/` directory using Jupyter Notebook or JupyterLab.

## Usage

To use the project, follow these steps:

0. Always run the programs from the root folder i.e. end to end ML/

1. Ensure that you have the necessary dataset available. If you have your own dataset, place it in the `notebook/` directory. Alternatively, you can modify the code to load the dataset from a different location.

2. Explore the provided Jupyter notebooks in the `notebooks/` directory. These notebooks provide a step-by-step guide on data preprocessing, feature engineering, model development, and evaluation.

3. Execute the cells in the notebooks to run the code and observe the results. Modify the code as needed to experiment with different techniques or algorithms.

4. Once you have trained a model and are satisfied with the results, you can save the model to the `models/` directory using the appropriate functions provided in the code.

5. If you have created or modified any source code files or scripts in the `src/` directory, you can run them as standalone scripts or import them into the notebooks for reuse.

## Contributing

If you wish to contribute to this project, please follow these guidelines:

1. Fork the repository to your own GitHub account.

2. Create a new branch with a descriptive name for your contribution.

3. Make your changes and improvements to the project.

4. Test your changes thoroughly and ensure that the project still runs without issues.

5. Commit and push your changes to your forked repository.

6. Submit a pull request with a clear description of your changes and why they should be merged.

### CICD using Github actions with AWS
## End to End MAchine Learning Project

1. Docker Build checked
2. Github Workflow
3. Iam User In AWS

## Docker Setup In EC2 commands to be Executed

#optinal

sudo apt-get update -y

sudo apt-get upgrade

#required

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

## Configure EC2 as self-hosted runner:

## Setup github secrets:
1.
2.
3.
4.
5.


## License

The project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code for both commercial and non-commercial purposes.

## Acknowledgements

If applicable, provide acknowledgements to any individuals, resources, or libraries that were instrumental in the development of this project.

## Contact

For any questions or inquiries, please contact Chandan Kumar at chandankr014@gmail.com or ping on wa.me/917070957221.
