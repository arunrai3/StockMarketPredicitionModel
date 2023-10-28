


def histogram(n_20_plus, n_0_20_plus,n_0_20_minus, n_20_minus, ax):
    bins2 = [-40,-20,0,20,40]
    returns = []
    
    
    for key, value in n_20_plus.items():
        returns.append(25)    
    for key, value in n_0_20_plus.items():
        returns.append(value)    
    for key, value in n_0_20_minus.items():
        returns.append(value)    
    for key, value in n_20_minus.items():
        returns.append(-25)    
    
    

    ax.hist(returns, bins=bins2, edgecolor='black')

    x_ticks = [-40, -20, 0, 20, 40]  
    
    x_tick_labels = ['<-40%', '-20%', '0%', '20%', '>40%']
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)
    
    
    #plt.legend(['n_20_plus', 'n_0_20_plus', 'n_0_20_minus', 'n_20_minus'])
    ax.set_title('Percentage Return Each Year', fontsize=12)
    ax.set_xlabel('Percentage Return')
    ax.set_ylabel('Total Years')