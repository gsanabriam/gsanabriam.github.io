def miprimerdashboard() :
    ## 1. Llama librerias
      import pandas as pd
      import datetime as fecha
      import matplotlib.pyplot as plt
      from ipywidgets import interact, interactive
      import ipywidgets as widgets
      import numpy as np
      #from datetime import datetime
      import datetime as dt
      import seaborn as sns
      from IPython.display import HTML, display_html, display
      ## 2. Lee base de dastos
      df=pd.read_excel("BaseCovid.xlsx")
      ## 3. Elimina Blancos
      df["Estado"]=[i.replace(" ","") for i in df["Estado"]]# Armando una lista que corrige el error de digitación
      ## 4. Remplaza Fallecidos
      df["Estado"]=[i.replace("FallecidoNoaplicaNocausaDirecta","Fallecido") for i in df["Estado"]]# Corrige Fallecido
      ##5. Ajusta nombre localidad
      df= df.rename(columns={'Localidad de residencia':'Localidad'})
      ##6. Genera variable Meses
      df['Meses'] = df['Fecha de diagnóstico'].apply(lambda x: 
                                    dt.datetime.strftime(x,'%Y%m'))

      ## Comienza el dashboard
      display(HTML('<center><h1> DASHBOARD COVID-19</h1></Center>'))

      def f(localidad,Estado):
          df2=df[(df["Localidad"]==localidad) &  (df["Estado"]==Estado) ]
          df3=df2.groupby("Meses")["Estado"].count()
          df4=pd.DataFrame(df3)

          display(HTML('<h2> 1. Evolución estados del Covid-19 </h2>')) 

          # Gráficos Lineas
          fig, ax = plt.subplots()
          ax.plot(df4.index, df4.values)
          plt.xlabel('Mes de Diagnostico')
          plt.ylabel('Cantidad de pacientes')
          plt.show()
          # Gráfico Barras Genero
          display(HTML('<h2> 2. Cantidad de casos por genero </h2>')) 
          plt.figure(figsize=(10,8))
          ax = sns.countplot(x="Meses", hue="Sexo", data=df2)
          plt.ylabel('Total de personas')
          plt.xlabel("Mes de diagnóstico")
          plt.legend(loc='upper left')
          for p in ax.patches:
              x=p.get_bbox().get_points()[:,0]
              y=p.get_bbox().get_points()[1,1]
              ax.annotate('{:,}'.format(y), (x.mean(), y), 
                      ha='center', va='bottom')         
          
      #Localidad
      Loca=widgets.Dropdown(
          options=df.Localidad.unique().tolist(),
          description='Localidad:',
          disabled=False,)
      #Estado
      Est=widgets.Dropdown(
            options=df.Estado.unique().tolist(),
            description='Estado:',
            disabled=False,)

      interact(f, localidad=Loca,Estado=Est)
      return