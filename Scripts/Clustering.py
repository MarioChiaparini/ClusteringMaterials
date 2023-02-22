from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from TesteGetData import BatteryDF
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import silhouette_score
from matplotlib.colors import ListedColormap 

new_df = BatteryDF('_Na')

x = new_df.iloc[:,0:2]
y = new_df['Formula']

label = LabelEncoder()
label.fit(y)

y = label.transform(y)

minmax = MinMaxScaler()
x = minmax.fit_transform(x)

columns = ['Grav. Energy', 'Grav. Capacity']

minmax = MinMaxScaler()
x = minmax.fit_transform(x)
x = pd.DataFrame(x, columns=[columns])

plt.scatter(x['Grav. Capacity'], x['Grav. Energy'])

#Elbow Method
cost = []
for i in range(1, 11):
    KM = KMeans(n_clusters = i, max_iter = 500)
    KM.fit(x['Grav. Energy'])
    cost.append(KM.inertia_)    
plt.plot(range(1, 11), cost, color ='g', linewidth ='3')
plt.xlabel("Value of K")
plt.ylabel("Squared Error (Cost)")
plt.show() # clear the plot


Kmean= KMeans(n_clusters=3, init='k-means++', random_state=42)
y = Kmean.fit_predict(x)

score = silhouette_score(x,y)
print(score)


#plt.scatter(y, x['Grav. Capacity'], c=Kmean.labels_, cmap='rainbow')
new_df['Cluster'] = y
unique_labels = new_df["Cluster"].unique()
cl0 =  new_df[new_df.Cluster==unique_labels[1]]
cl1 = new_df[new_df.Cluster==unique_labels[0]]
#cl2 = new_df[new_df.Cluster==unique_labels[2]]
#cl3 = new_df[new_df.Cluster==unique_labels[4]]
#cl4 = new_df[new_df.Cluster==unique_labels[0]]
cl0.to_csv('HighestCluserMaterial.csv')

#cl0['Grav. Energy'].idxmax()
max_row = cl0.loc[cl0['Grav. Energy'].idxmax()]

customcmap = ListedColormap(["crimson", "mediumblue", "darkmagenta"])
fig, ax = plt.subplots(figsize=(8, 6))
plt.scatter(x=new_df['Grav. Capacity'], y=new_df['Grav. Energy'], s=150,
            c=new_df['Cluster'].astype('category'), 
            cmap = customcmap)
ax.set_xlabel(r'Capacity', fontsize=14)
ax.set_ylabel(r'Energy', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()



