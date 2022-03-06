import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
import numpy as np

def plot_alation():
    target=['Inc-v3','Inc-v4','IncRes-v2','Res-152']
    #old
    # inc_abs=[97.8,68.0,58.9,36.9,49.7,26.9,12.6,5.7]
    # inc_grad=[93.9,56.7,54.5,37.8,45.0,29.0,21.8,12.4]
    # inc_ens_grad=[98.0,81.4,79.7,60.2,69.6,48.8,33.4,17.5]
    #old
    # vgg_abs=[71.7,71.9,56.6,72.1,92.7,48.5,32.0,54.1]
    # vgg_grad=[89.0,88.6,84.6,89.8,99.9,73.3,55.1,76.5]
    # vgg_ens_grad=[94.5,95.7,92.3,95.5,100.0,82.3,64.8,85.9]
    #new
    # inc_abs=[90.1, 59.2, 52.8, 32.3, 40.0, 25.6, 11.8, 5.5]
    # inc_grad=[93.3, 58.0, 56.0, 38.6, 49.8, 30.5, 24.6, 13.1]
    # inc_ens_grad=[98.1, 83.4, 80.7, 62.7, 72.1, 54.4, 36.2, 18.6]
    #new
    vgg_abs=[71.5,69.6,56.4,72.4]
    # vgg_grad=[90.3,91.0,87.4,90.6,99.5,78.7,76.2,59.6]
    # vgg_ens_grad=[95.5, 96.2, 92.5, 95.0,99.9,84.8,79.6,61.1]

    fig, ax=plt.subplots(figsize=(8,3))

    x=np.arange(len(target))
    width=0.15

    # plt.bar(x,inc_abs,width=width,hatch = '/',edgecolor = 'white',label='L1',color='steelblue')
    # plt.bar(x+width,inc_grad,width=width,hatch='\\',edgecolor = 'white',label='L2',color='indianred',tick_label=target)
    # plt.bar(x+2*width,inc_ens_grad,width=width,hatch='.',edgecolor = 'white',label='L3',color='darkseagreen')

    plt.bar(x,vgg_abs,width=width,hatch = '/',edgecolor = 'white',label='L1',color='steelblue')
    # plt.bar(x+width,vgg_grad,width=width,hatch='\\',edgecolor = 'white',label='L2',color='indianred',tick_label=target)
    # plt.bar(x+2*width,vgg_ens_grad,width=width,hatch='.',edgecolor = 'white',label='L3',color='darkseagreen')

    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # plt.grid(axis='y',linestyle='-.', linewidth=1,color='lightgray')

    #Times New Roman
    plt.xticks(rotation=0)
    plt.tick_params(labelsize=8)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('serif') for label in labels]

    plt.legend(loc="upper right",prop={"family" : "serif",  'size':8})  # 防止label和图像重合显示不出来
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.ylabel('Attack Success Rate', fontdict={'family':'serif','size': 9})
    plt.xlabel('Target Model',fontdict={'family':'serif','size': 9})
    # plt.title("Source Model: Inc-v3",fontdict={'family':'serif','size': 9})
    plt.title('Source Model: Vgg-16',fontdict={'family':'serif','size': 9})
    plt.show()




if __name__ == '__main__':
    # plot_ens_prob()
    # plot_heatmap()
    # hyper_plot()
    # layer_plot()
    plot_alation()
