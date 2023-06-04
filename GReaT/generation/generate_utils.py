import matplotlib.pyplot as plt
import pandas as pd
from be_great import GReaT
from be_great.great_trainer import GReaTTrainer



def start_generation(data: pd.DataFrame, folder_name: str, drop_columns_list: list, epochs: int = 250, batch_size: int = 32,
                conditional_column : str = None):
    """
    Calls the functions to train the model plot the learning history and sample different sizes of synthetic data.

    Parameters
    ----------
    data : pd.DataFrame
        Tabular data on which the synthesized data is based on
    folder_name : str
        The folder in which the input file is stored and the output will be saved.
    drop_columns_list : list, optional
        Defines columns which will be dropped
    epochs : int
        Number of epochs for fine-tuning (default : 250)
    batch_size : int
        Batch size for fine-tuning (default : 32)
    conditional_column : str
        Sampling will depend on that column (default : last column)
    """

    trainer = train_model(data, folder_name, drop_columns_list, epochs, batch_size, conditional_column)

    plot_history(trainer, folder_name, epochs)

    for number_of_samples in [100, 1000, 10000]:
        sample_model(folder_name, number_of_samples, batch_size)


def train_model(data: pd.DataFrame, folder_name: str, drop_columns_list: list, epochs: int = 250, batch_size: int = 32,
                conditional_column : str = None):
    """
    Optionally drops columns and fine-tunes the model based on the distilgpt2 HuggingFace checkpoint.

    Parameters
    ----------
    data : pd.DataFrame
        Used to train the model
    folder_name : str
        Defines the folder where the training checkpoints will be stored
    drop_columns_list : list
        Contains column names which will be dropped
    epochs : int
        Number of epochs for fine-tuning (default : 250)
    batch_size : int
        Batch size for fine-tuning (default : 32)
    conditional_column : str
        Sampling will depend on that column (default : last column)

    Returns
    -------
    GReaTTrainer used for the fine-tuning process
    """

    if len(drop_columns_list) != 0:
        data.drop(drop_columns_list, axis=1, inplace=True)

    experiment_dir = f"./{folder_name}/trainer_{folder_name}"
    great = GReaT(llm="distilgpt2", batch_size=batch_size, epochs=epochs, save_steps=epochs * 2,
                  logging_steps=epochs / 2, experiment_dir=experiment_dir)
    trainer = great.fit(data, conditional_column)
    great.save(folder_name)

    return trainer


def plot_history(trainer : GReaTTrainer, folder_name : str, global_epochs : int = 250):
    """
    Plots the learning curve in a line chart to check overfitting/underfitting.

    Parameters
    ----------
    trainer : GReaTTrainer
        Trainer utilized for training
    folder_name : str
        Folder and name of the result for storage purposes
    global_epochs
        Number of epochs for storage purposes (default : 250)
    """
    loss_hist = trainer.state.log_history.copy()
    loss_hist.pop()

    loss = [x["loss"] for x in loss_hist]
    epochs = [x["epoch"] for x in loss_hist]

    plt.plot(epochs, loss)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title(f"Learning curve for {global_epochs} epochs")

    figure = plt.gcf()
    figure.savefig(f"./{folder_name}/{folder_name}_learning_curve_{global_epochs}.png")
    plt.show()


def sample_model(folder_name: str, number_of_samples: int = 100, sampling_batch_size: int = 32):
    """
    Generates synthetic data samples and saves them in the folder.

    Parameters
    ----------
    folder_name :
        Folder name of where the trainer is saved and the samples will be stored
    number_of_samples : int
        Number of synthetic data points which will be generated (default : 100)
    sampling_batch_size : int
        Batch size used for sampling (default : 32)
    """
    great = GReaT.load_from_dir(folder_name)
    samples = great.sample(number_of_samples, k=sampling_batch_size)
    samples.to_csv(f"./{folder_name}/{folder_name}_samples_{number_of_samples}.csv")

