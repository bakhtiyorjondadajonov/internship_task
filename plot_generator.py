import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class PlotGenerator:
    def __init__(self,json_file:str):
        self.json_file=json_file
        self.df=None
        self.plots_dir='plots'
    def load_data(self):
        self.df=pd.read_json(self.json_file)
        print('Data loaded sucessfully!')
        if not os.path.exists(self.plots_dir):
            os.makedirs(self.plots_dir)   
    def calc_MAE(self):
        self.df['corner_error'] = abs(self.df['gt_corners'] - self.df['rb_corners'])
        mae_corners = self.df['corner_error'].mean()

        # Accuracy
        accuracy = (self.df['corner_error'] == 0).mean() * 100

        print(f"MAE (Corner Predictions): {mae_corners}")
        print(f"Accuracy: {accuracy}%")        
    def draw_plots(self):
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() before drawing plots.")
        saved_paths = []

        # 1. Histogram of Overall Deviations (Mean, Max, Min)
        plt.figure(figsize=(15, 5))
        for i, col in enumerate(['mean', 'max', 'min']):
            plt.subplot(1, 3, i + 1)
            sns.histplot(self.df[col], kde=True, bins=30, color="skyblue")
            plt.title(f'Distribution of {col.capitalize()} Deviation')
            plt.xlabel('Degrees')
            plt.ylabel('Frequency')

        plt.tight_layout()
        plot_path = os.path.join(self.plots_dir, 'histogram_mean_deviation.png')
        plt.savefig(plot_path)
        plt.close()
        saved_paths.append(plot_path)
        # 2. Boxplots for Floor vs Ceiling Deviation Means
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.df[['floor_mean', 'ceiling_mean']], palette="pastel")
        plt.title('Floor vs Ceiling Mean Deviations')
        plt.ylabel('Degrees')
        plt.xticks(ticks=[0, 1], labels=['Floor Mean', 'Ceiling Mean'])
        plot_path = os.path.join(self.plots_dir, 'boxplots_for_floor_vs_ceiling_deviation.png')
        plt.savefig(plot_path)
        plt.close()
        saved_paths.append(plot_path)
        # 3. Scatter Plot: Floor Mean vs Ceiling Mean
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x='floor_mean', y='ceiling_mean', data=self.df, alpha=0.6, color='purple')
        plt.title('Floor Mean vs Ceiling Mean Deviations')
        plt.xlabel('Floor Mean Deviation (Degrees)')
        plt.ylabel('Ceiling Mean Deviation (Degrees)')
        plt.axline((0, 0), slope=1, color='red', linestyle='--', label='y = x')
        plt.legend()
        plot_path = os.path.join(self.plots_dir, 'scatter_plot_floor_mean_vs_ceiling.png')
        plt.savefig(plot_path)
        plt.close()
        saved_paths.append(plot_path)

        print('Plots have been created and saved in the plots folder!')

