from django.shortcuts import render
import plotly.express as px
import json
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# from charts.forms import DateForm

# Create your views here.
# самый базовый синтаксис отрисовки чартов
# pd.set_option("display.max.columns", None)
pd.options.plotting.backend='plotly'

with open('/Users/ves/django-plotly/dp/charts/data/student_new_add.json', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    string_json = "".join([k.lstrip('\ufeff') for k in lines])
    data = json.loads(string_json)

df = pd.DataFrame(data)
df = df.replace(to_replace='Среднее профессиональное образование', value='СПО')

def proflvls(request):

    df1 = df.groupby(['ДатаНачалаОбучения','УровеньПодготовки'], as_index=True).count()
    df1 = df1.filter(like='.2020', axis=0) # 1 - по столбцам, 0 - по строкам.
    df1 = df1.reset_index(level=['ДатаНачалаОбучения','УровеньПодготовки'])
    df1 = df1.assign(ГодНачалаОбучения = '2020')
    df1 = df1.groupby(['УровеньПодготовки', "ГодНачалаОбучения"], as_index=False).sum()

    df2 = df.groupby(['ДатаНачалаОбучения','УровеньПодготовки'], as_index=True).count()
    df2 = df2.filter(like='.2021', axis=0) # 1 - по столбцам, 0 - по строкам.
    df2 = df2.reset_index(level=['ДатаНачалаОбучения','УровеньПодготовки'])
    df2 = df2.assign(ГодНачалаОбучения = '2021')
    df2 = df2.groupby(['УровеньПодготовки', "ГодНачалаОбучения"], as_index=False).sum()

    df3 = df.groupby(['ДатаНачалаОбучения','УровеньПодготовки'], as_index=True).count()
    df3 = df3.filter(like='.2022', axis=0) # 1 - по столбцам, 0 - по строкам.
    df3 = df3.reset_index(level=['ДатаНачалаОбучения','УровеньПодготовки'])
    df3 = df3.assign(ГодНачалаОбучения = '2022')
    df3 = df3.groupby(['УровеньПодготовки', "ГодНачалаОбучения"], as_index=False).sum()

    df4 = pd.concat([df1, df2, df3], ignore_index=True)
    df4 = df4.sort_values(["ГодНачалаОбучения", 'GUID'], ascending=True)


    # Строим график
    fig1 = px.bar(df4, x="ГодНачалаОбучения", y="GUID", color="УровеньПодготовки", 
                    text_auto=True, labels={'GUID':'Зачислено студентов'}, #height=800, 
                    barmode="group", color_discrete_sequence=px.colors.qualitative.Pastel)
    proflvls = fig1.to_html()                  
    context = {'proflvls': proflvls}#, 'form': DateForm()}
    return render(request, 'proflvls.html', context)

def directions(request):
    def get_dirs(dirs, hgt):
        df11 = df.loc[df['УровеньПодготовки'] == dirs]
        df11 = df11.groupby(['ДатаНачалаОбучения', 'Направление'], as_index=True).count()
        df11 = df11.filter(like='.2020', axis=0) # 1 - по столбцам, 0 - по строкам.
        df11 = df11.reset_index(level=['ДатаНачалаОбучения', 'Направление'])
        df11 = df11.assign(ГодНачалаОбучения = '2020')
        df11 = df11.groupby(['Направление', "ГодНачалаОбучения"], as_index=False).sum()
        
        df12 = df.loc[df['УровеньПодготовки'] == dirs]
        df12 = df12.groupby(['ДатаНачалаОбучения', 'Направление'], as_index=True).count()
        df12 = df12.filter(like='.2021', axis=0) # 1 - по столбцам, 0 - по строкам.
        df12 = df12.reset_index(level=['ДатаНачалаОбучения','Направление'])
        df12 = df12.assign(ГодНачалаОбучения = '2021')
        df12 = df12.groupby(['Направление', "ГодНачалаОбучения"], as_index=False).sum()

        df13 = df.loc[df['УровеньПодготовки'] == dirs]
        df13 = df13.groupby(['ДатаНачалаОбучения','Направление'], as_index=True).count()
        df13 = df13.filter(like='.2022', axis=0) # 1 - по столбцам, 0 - по строкам.
        df13 = df13.reset_index(level=['ДатаНачалаОбучения','Направление'])
        df13 = df13.assign(ГодНачалаОбучения = '2022')
        df13 = df13.groupby(['Направление', "ГодНачалаОбучения"], as_index=False).sum()

        df9 = pd.concat([df11, df12, df13], ignore_index=False)
        fig3 = px.bar(df9, y="GUID", x="Направление", 
                        color="ГодНачалаОбучения", 
                        text_auto=True, 
                        labels={'GUID':'Зачислено студентов', 
                                "ГодНачалаОбучения": dirs,
                                'Направление': '' }, 
                        height=hgt,
                        color_discrete_sequence=px.colors.qualitative.Pastel)
        fig3.update_layout(xaxis_tickangle=45)
        return fig3

    bachelor_degree = get_dirs("Бакалавриат", 1000)
    master_degree = get_dirs("Магистратура", 1000)
    phd_degree = get_dirs("Аспирантура", 1000)
    specialist_degree = get_dirs("Специалитет", 800)
    vocational_degree = get_dirs("СПО", 1000)
    residency_degree = get_dirs("Ординатура", 600)

    bach_dir = bachelor_degree.to_html()                  
    mas_dir = master_degree.to_html()    
    phd_dir = phd_degree.to_html()    
    spec_dir = specialist_degree.to_html()    
    voc_dir = vocational_degree.to_html()    
    res_dir = residency_degree.to_html()    

    context = {'bach_dir': bach_dir, 
                'mas_dir': mas_dir, 
                'phd_dir': phd_dir, 
                'spec_dir': spec_dir,
                'voc_dir': voc_dir, 
                'res_dir': res_dir}
    return render(request, 'directions.html', context)

def foreigns(request):
    df14 = df.loc[df['Гражданство'] != 'РОССИЯ']
    df14 = df14.loc[df14['Гражданство'] != 'Российская Федерация']


    df15 = df14.groupby(['ДатаНачалаОбучения', 'Гражданство'], as_index=True).count()
    df15 = df15.filter(like='.2020', axis=0) # 1 - по столбцам, 0 - по строкам.
    df15 = df15.reset_index(level=['ДатаНачалаОбучения','Гражданство'])
    df15 = df15.assign(ГодНачалаОбучения = '2020')
    df15 = df15.groupby(['Гражданство', "ГодНачалаОбучения"], as_index=False).sum()

    df16 = df14.groupby(['ДатаНачалаОбучения', 'Гражданство'], as_index=True).count()
    df16 = df16.filter(like='.2021', axis=0) # 1 - по столбцам, 0 - по строкам.
    df16 = df16.reset_index(level=['ДатаНачалаОбучения','Гражданство'])
    df16 = df16.assign(ГодНачалаОбучения = '2021')
    df16 = df16.groupby(['Гражданство', "ГодНачалаОбучения"], as_index=False).sum()

    df17 = df14.groupby(['ДатаНачалаОбучения', 'Гражданство'], as_index=True).count()
    df17 = df17.filter(like='.2022', axis=0) # 1 - по столбцам, 0 - по строкам.
    df17 = df17.reset_index(level=['ДатаНачалаОбучения','Гражданство'])
    df17 = df17.assign(ГодНачалаОбучения = '2022')
    df17 = df17.groupby(['Гражданство', "ГодНачалаОбучения"], as_index=False).sum()

    df18 = pd.concat([df15, df16, df17], ignore_index=False)
    df18 = df18.sort_values(['Гражданство'], ascending=False)


    fig4 = px.bar(df18, x='GUID', y='Гражданство', 
                    color='ГодНачалаОбучения', 
                    text_auto=True, height=1500, 
                    labels={'GUID':'Зачислено студентов'},
                    color_discrete_sequence=px.colors.qualitative.Pastel)
    # fig4.update_layout(xaxis_tickangle=45)
    foreigns = fig4.to_html()                  
    context = {'foreigns': foreigns}
    return render(request, 'foreigns.html', context)

def forms(request):
    def get_form(form, wdt=None):
        df2_1 = df.groupby(['ДатаНачалаОбучения','ФормаОбучения', 'УровеньПодготовки'], as_index=True).count() 
        df2_1 = df2_1.filter(like='2020', axis=0) # 1 - по столбцам, 0 - по строкам.
        df2_1 = df2_1.reset_index(level=['ДатаНачалаОбучения','ФормаОбучения', 'УровеньПодготовки'])
        df2_1 = df2_1.assign(ГодНачалаОбучения = '2020')
        df2_1 = df2_1.groupby(['ФормаОбучения', "ГодНачалаОбучения", 'УровеньПодготовки'], as_index=False).sum()
        df2_1 = df2_1.loc[df2_1['ФормаОбучения'] == form]
        df2_1 = df2_1.sort_values(['GUID'], ascending=True)

        df2_2 = df.groupby(['ДатаНачалаОбучения','ФормаОбучения', 'УровеньПодготовки'], as_index=True).count() 
        df2_2 = df2_2.filter(like='2021', axis=0) # 1 - по столбцам, 0 - по строкам.
        df2_2 = df2_2.reset_index(level=['ДатаНачалаОбучения','ФормаОбучения', 'УровеньПодготовки'])
        df2_2 = df2_2.assign(ГодНачалаОбучения = '2021')
        df2_2 = df2_2.groupby(['ФормаОбучения', "ГодНачалаОбучения", 'УровеньПодготовки'], as_index=False).sum()
        df2_2 = df2_2.loc[df2_2['ФормаОбучения'] == form]
        df2_2 = df2_2.sort_values(['GUID'], ascending=True)

        df2_3 = df.groupby(['ДатаНачалаОбучения','ФормаОбучения', 'УровеньПодготовки'], as_index=True).count() 
        df2_3 = df2_3.filter(like='2022', axis=0) # 1 - по столбцам, 0 - по строкам.
        df2_3 = df2_3.reset_index(level=['ДатаНачалаОбучения','ФормаОбучения', 'УровеньПодготовки'])
        df2_3 = df2_3.assign(ГодНачалаОбучения = '2022')
        df2_3 = df2_3.groupby(['ФормаОбучения', "ГодНачалаОбучения", 'УровеньПодготовки'], as_index=False).sum()
        df2_3 = df2_3.loc[df2_3['ФормаОбучения'] == form]
        df2_3 = df2_3.sort_values(['GUID'], ascending=True)

        df2_4 = pd.concat([df2_1, df2_2, df2_3], ignore_index=True)

        fig2_1 = px.bar(df2_4, x='ГодНачалаОбучения', y='GUID', color='УровеньПодготовки', 
                        text_auto=True, labels={'GUID':'Зачислено студентов', 
                                                'УровеньПодготовки': form,
                                                'ГодНачалаОбучения': 'Год начала обучения'}, 
                        barmode="group", color_discrete_sequence=px.colors.qualitative.Pastel,
                        width=wdt)
        return fig2_1

    fulltime = get_form('Очная')
    extramural = get_form('Заочная')
    parttime = get_form('Очно-заочная')

    ft = fulltime.to_html()                  
    em = extramural.to_html()                  
    pt = parttime.to_html()

    context = {'ft': ft, 'em': em, 'pt': pt}
    return render(request, 'forms.html', context)

def basics(request):
    def get_basic(basic, wdt=None):
        df5_1 = df.groupby(['ДатаНачалаОбучения','Основа', 'УровеньПодготовки'], as_index=True).count() 
        df5_1 = df5_1.filter(like='2020', axis=0) # 1 - по столбцам, 0 - по строкам.
        df5_1 = df5_1.reset_index(level=['ДатаНачалаОбучения','Основа', 'УровеньПодготовки'])
        df5_1 = df5_1.assign(ГодНачалаОбучения = '2020')
        df5_1 = df5_1.groupby(['Основа', "ГодНачалаОбучения", 'УровеньПодготовки'], as_index=False).sum()
        df5_1 = df5_1.loc[df5_1['Основа'] == basic]
        df5_1 = df5_1.sort_values(['GUID'], ascending=True)

        df5_2 = df.groupby(['ДатаНачалаОбучения','Основа', 'УровеньПодготовки'], as_index=True).count() 
        df5_2 = df5_2.filter(like='2021', axis=0) # 1 - по столбцам, 0 - по строкам.
        df5_2 = df5_2.reset_index(level=['ДатаНачалаОбучения','Основа', 'УровеньПодготовки'])
        df5_2 = df5_2.assign(ГодНачалаОбучения = '2021')
        df5_2 = df5_2.groupby(['Основа', "ГодНачалаОбучения", 'УровеньПодготовки'], as_index=False).sum()
        df5_2 = df5_2.loc[df5_2['Основа'] == basic]
        df5_2 = df5_2.sort_values(['GUID'], ascending=True)

        df5_3 = df.groupby(['ДатаНачалаОбучения','Основа', 'УровеньПодготовки'], as_index=True).count() 
        df5_3 = df5_3.filter(like='2022', axis=0) # 1 - по столбцам, 0 - по строкам.
        df5_3 = df5_3.reset_index(level=['ДатаНачалаОбучения','Основа', 'УровеньПодготовки'])
        df5_3 = df5_3.assign(ГодНачалаОбучения = '2022')
        df5_3 = df5_3.groupby(['Основа', "ГодНачалаОбучения", 'УровеньПодготовки'], as_index=False).sum()
        df5_3 = df5_3.loc[df5_3['Основа'] == basic]
        df5_3 = df5_3.sort_values(['GUID'], ascending=True)

        df5_4 = pd.concat([df5_1, df5_2, df5_3], ignore_index=True)

        fig5 = px.bar(df5_4, x='ГодНачалаОбучения', y='GUID', color='УровеньПодготовки', 
                        text_auto=True, labels={'GUID':'Зачислено студентов', 
                                                'УровеньПодготовки': basic,
                                                'ГодНачалаОбучения': 'Год начала обучения'}, 
                        barmode="group", color_discrete_sequence=px.colors.qualitative.Pastel,
                        width=wdt)
        return fig5

    bas1 = get_basic('Бюджетная основа')
    bas2 = get_basic('Полное возмещение затрат')
    bas3 = get_basic('Целевой прием')

    basics1 = bas1.to_html()                  
    basics2 = bas2.to_html()                  
    basics3 = bas3.to_html()                  
                
    context = {'basics1': basics1, 'basics2': basics2, 'basics3': basics3 }
    return render(request, 'basics.html', context)


def registrations(request):
    df01 = df[df['АдресРегистрации'].str.contains('Калининградская')]
    df01 = df01.groupby(['ДатаНачалаОбучения'], as_index=True).count() 
    df01 = df01.filter(like='2020', axis=0)
    df01 = df01.reset_index(level=['ДатаНачалаОбучения'])
    df01 = df01.assign(ГодНачалаОбучения = '2020')
    df01 = df01.assign(Прописка = 'К.О.')
    df01 = df01.groupby(["ГодНачалаОбучения", 'Прописка'], as_index=False).sum()
    # df01
    df02 = df[df["АдресРегистрации"].str.contains("Калининградская") == False]
    df02 = df02.groupby(['ДатаНачалаОбучения'], as_index=True).count() 
    df02 = df02.filter(like='2020', axis=0)
    df02 = df02.reset_index(level=['ДатаНачалаОбучения'])
    df02 = df02.assign(ГодНачалаОбучения = '2020')
    df02 = df02.assign(Прописка = 'Другая')
    df02 = df02.groupby(["ГодНачалаОбучения", 'Прописка'], as_index=False).sum()

    df_03 = pd.concat([df01, df02], ignore_index=True)

    df03 = df[df['АдресРегистрации'].str.contains('Калининградская')]
    df03 = df03.groupby(['ДатаНачалаОбучения'], as_index=True).count() 
    df03 = df03.filter(like='2021', axis=0)
    df03 = df03.reset_index(level=['ДатаНачалаОбучения'])
    df03 = df03.assign(ГодНачалаОбучения = '2021')
    df03 = df03.assign(Прописка = 'К.О.')
    df03 = df03.groupby(["ГодНачалаОбучения", 'Прописка'], as_index=False).sum()
    # df01
    df04 = df[df["АдресРегистрации"].str.contains("Калининградская") == False]
    df04 = df04.groupby(['ДатаНачалаОбучения'], as_index=True).count() 
    df04 = df04.filter(like='2021', axis=0)
    df04 = df04.reset_index(level=['ДатаНачалаОбучения'])
    df04 = df04.assign(ГодНачалаОбучения = '2021')
    df04 = df04.assign(Прописка = 'Другая')
    df04 = df04.groupby(["ГодНачалаОбучения", 'Прописка'], as_index=False).sum()

    df_05 = pd.concat([df03, df04], ignore_index=True)

    df06 = df[df['АдресРегистрации'].str.contains('Калининградская')]
    df06 = df06.groupby(['ДатаНачалаОбучения'], as_index=True).count() 
    df06 = df06.filter(like='2022', axis=0)
    df06 = df06.reset_index(level=['ДатаНачалаОбучения'])
    df06 = df06.assign(ГодНачалаОбучения = '2022')
    df06 = df06.assign(Прописка = 'К.О.')
    df06 = df06.groupby(["ГодНачалаОбучения", 'Прописка'], as_index=False).sum()
    # df01
    df07 = df[df["АдресРегистрации"].str.contains("Калининградская") == False]
    df07 = df07.groupby(['ДатаНачалаОбучения'], as_index=True).count() 
    df07 = df07.filter(like='2022', axis=0)
    df07 = df07.reset_index(level=['ДатаНачалаОбучения'])
    df07 = df07.assign(ГодНачалаОбучения = '2022')
    df07 = df07.assign(Прописка = 'Другая')
    df07 = df07.groupby(["ГодНачалаОбучения", 'Прописка'], as_index=False).sum()

    df_08 = pd.concat([df06, df07], ignore_index=True)

    df_09 = pd.concat([df_03, df_05, df_08], ignore_index=True)

    fig22 = px.bar(df_09, x='ГодНачалаОбучения', y='GUID', color='Прописка', 
                    text_auto=True, labels={'GUID':'Зачислено студентов'}, 
                    barmode="group", color_discrete_sequence=px.colors.qualitative.Pastel)
    # fig2_1.show()
    reg = fig22.to_html() 
    context = {'reg': reg}
    return render(request, 'registrations.html', context)