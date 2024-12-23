import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from typing import List, Dict, Any
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection with pooling and retry logic
@st.cache_resource
def get_db_engine():
    """Create and cache database engine."""
    return create_engine(
        f"postgresql://{st.secrets['postgres']['user']}:{st.secrets['postgres']['password']}"
        f"@{st.secrets['postgres']['host']}:{st.secrets['postgres']['port']}"
        f"/{st.secrets['postgres']['database']}"
    )

@st.cache_data
def get_filtered_data(_engine, field: str, il: str = None, ilce: str = None, 
                     mahalle: str = None, ada: str = None) -> list:
    """Get filtered data from database using SQLAlchemy."""
    query = f'SELECT DISTINCT "{field}" FROM zemin WHERE 1=1'
    params = {}
    
    if il and field != 'Il':
        query += ' AND "Il" = :il'
        params['il'] = il
    if ilce and field not in ['Il', 'Ilce']:
        query += ' AND "Ilce" = :ilce'
        params['ilce'] = ilce
    if mahalle and field not in ['Il', 'Ilce', 'MahalleKoyAdi']:
        query += ' AND "MahalleKoyAdi" = :mahalle'
        params['mahalle'] = mahalle
    if ada and field not in ['Il', 'Ilce', 'MahalleKoyAdi', 'Ada']:
        query += ' AND "Ada" = :ada'
        params['ada'] = ada
        
    query += f' ORDER BY "{field}"'
    
    try:
        with _engine.connect() as conn:
            result = conn.execute(text(query), params)
            return [row[0] for row in result if row[0]]
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        st.error("Veritabanına erişimde bir hata oluştu. Lütfen tekrar deneyin.")
        return []

def search_records(_engine, il: str, ilce: str, mahalle: str, ada: str, parsel: str) -> pd.DataFrame:
    """Search records with SQLAlchemy."""
    query = """
    SELECT 
        z."ParselRef",
        z."Il",
        z."Ilce",
        z."MahalleKoyAdi",
        z."Ada",
        z."Parsel",
        zh."Adi",
        zh."Soyadi",
        zh."BabaAdi",
        zh."TCKimlikNo",
        zh."HissePay",
        zh."HissePayda",
        CAST(CAST(zh."HissePay" AS FLOAT) / CAST(zh."HissePayda" AS FLOAT) * 100 AS DECIMAL(10,2)) as "HisseOrani"
    FROM zemin z
    INNER JOIN zeminhisse zh ON z."ID" = zh."ZeminRef"
    WHERE z."Il" = :il
    AND z."Ilce" = :ilce
    AND z."MahalleKoyAdi" = :mahalle
    AND z."Ada" = :ada
    AND z."Parsel" = :parsel
    ORDER BY zh."Adi", zh."Soyadi"
    """
    
    try:
        with _engine.connect() as conn:
            result = conn.execute(
                text(query),
                {"il": il, "ilce": ilce, "mahalle": mahalle, "ada": ada, "parsel": parsel}
            )
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        st.error("Veritabanına erişimde bir hata oluştu. Lütfen tekrar deneyin.")
        return pd.DataFrame()

def create_pie_chart(df: pd.DataFrame) -> go.Figure:
    """Create a pie chart of share distributions."""
    try:
        if df.empty:
            return None
        
        df = df.copy()  # Create a copy
        df['HisseOrani'] = df['HisseOrani'].astype(float)
        
        names = df.apply(lambda x: f"{x['Adi']} {x['Soyadi']}", axis=1)
        values = df['HisseOrani']
        
        fig = px.pie(
            values=values,
            names=names,
            title='Hisse Dağılımı (%)'
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            texttemplate="%{percent:.2f}%"
        )
        return fig
    except Exception as e:
        logger.error(f"Pie chart error: {str(e)}")
        return None

def create_bar_chart(df: pd.DataFrame) -> go.Figure:
    """Create a bar chart of share distributions."""
    try:
        if df.empty:
            return None
        
        df = df.copy()  # Create a copy
        df['HisseOrani'] = df['HisseOrani'].astype(float)
        
        names = df.apply(lambda x: f"{x['Adi']} {x['Soyadi']}", axis=1)
        values = df['HisseOrani']
        
        fig = px.bar(
            x=names,
            y=values,
            title='Hisse Dağılımı (Bar Grafik)',
            labels={'x': 'Hissedar', 'y': 'Hisse Oranı (%)'}
        )
        fig.update_traces(
            texttemplate='%{y:.2f}%', 
            textposition='outside'
        )
        return fig
    except Exception as e:
        logger.error(f"Bar chart error: {str(e)}")
        return None

def create_waterfall_chart(df: pd.DataFrame) -> go.Figure:
    """Create a waterfall chart showing cumulative shares."""
    try:
        if df.empty:
            return None
        
        df = df.copy()  # Create a copy
        df['HisseOrani'] = df['HisseOrani'].astype(float)
        
        df_sorted = df.sort_values('HisseOrani', ascending=True)
        names = df_sorted.apply(lambda x: f"{x['Adi']} {x['Soyadi']}", axis=1)
        values = df_sorted['HisseOrani']
        
        fig = go.Figure(go.Waterfall(
            name="Kümülatif Hisse Dağılımı",
            orientation="v",
            measure=["relative"] * len(df),
            x=names,
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            text=[f"{val:.2f}%" for val in values],
            textposition='outside'
        ))
        
        fig.update_layout(
            title='Kümülatif Hisse Dağılımı',
            xaxis_title="Hissedar",
            yaxis_title="Hisse Oranı (%)",
            showlegend=False
        )
        
        return fig
    except Exception as e:
        logger.error(f"Waterfall chart error: {str(e)}")
        return None

def export_to_excel(df: pd.DataFrame) -> bytes:
    """Export DataFrame to Excel bytes."""
    buffer = io.BytesIO()
    
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sonuçlar', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sonuçlar']
        
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'bg_color': '#D9E1F2',
            'border': 1
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            max_length = max(df[value].astype(str).apply(len).max(), len(str(value)))
            worksheet.set_column(col_num, col_num, max_length + 2)
    
    buffer.seek(0)
    return buffer.getvalue()

def main():
    try:
        # Page config
        st.set_page_config(
            page_title="Zemin Arama",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Hide Streamlit menu and footer
        hide_menu_style = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
        """
        st.markdown(hide_menu_style, unsafe_allow_html=True)
        
        # Title
        st.title("Zemin Arama")
        
        # Get database engine
        engine = get_db_engine()
        
        # Create columns for form fields
        col1, col2, col3 = st.columns(3)
        
        with col1:
            iller = get_filtered_data(engine, "Il")
            il = st.selectbox("İl", [""] + iller)
        
        with col2:
            ilceler = get_filtered_data(engine, "Ilce", il=il) if il else []
            ilce = st.selectbox("İlçe", [""] + ilceler)
        
        with col3:
            mahalleler = get_filtered_data(engine, "MahalleKoyAdi", il=il, ilce=ilce) if ilce else []
            mahalle = st.selectbox("Mahalle/Köy", [""] + mahalleler)
        
        col4, col5 = st.columns(2)
        
        with col4:
            adalar = get_filtered_data(engine, "Ada", il=il, ilce=ilce, mahalle=mahalle) if mahalle else []
            ada = st.selectbox("Ada", [""] + adalar)
        
        with col5:
            parseller = get_filtered_data(engine, "Parsel", il=il, ilce=ilce, mahalle=mahalle, ada=ada) if ada else []
            parsel = st.selectbox("Parsel", [""] + parseller)
        
        # Search button
        search_clicked = st.button("Ara")
        
        if search_clicked and all([il, ilce, mahalle, ada, parsel]):
            df = search_records(engine, il, ilce, mahalle, ada, parsel)
            
            if not df.empty:
                # Display results in a table
                st.subheader("Arama Sonuçları")
                st.dataframe(df, use_container_width=True)
                
                # Create visualization section
                st.subheader("Görselleştirmeler")
                
                # Create tabs for different visualizations
                tab1, tab2, tab3 = st.tabs(["Pasta Grafik", "Bar Grafik", "Kümülatif Dağılım"])
                
                with tab1:
                    pie_chart = create_pie_chart(df)
                    if pie_chart:
                        st.plotly_chart(pie_chart, use_container_width=True)
                    else:
                        st.warning("Pasta grafik oluşturulamadı.")
                
                with tab2:
                    bar_chart = create_bar_chart(df)
                    if bar_chart:
                        st.plotly_chart(bar_chart, use_container_width=True)
                    else:
                        st.warning("Bar grafik oluşturulamadı.")
                
                with tab3:
                    waterfall_chart = create_waterfall_chart(df)
                    if waterfall_chart:
                        st.plotly_chart(waterfall_chart, use_container_width=True)
                    else:
                        st.warning("Kümülatif grafik oluşturulamadı.")
                
                # Summary statistics
                st.subheader("Özet İstatistikler")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Toplam Hissedar", len(df))
                
                with col2:
                    st.metric("Ortalama Hisse (%)", f"{df['HisseOrani'].mean():.2f}")
                
                with col3:
                    st.metric("En Yüksek Hisse (%)", f"{df['HisseOrani'].max():.2f}")
                
                with col4:
                    st.metric("En Düşük Hisse (%)", f"{df['HisseOrani'].min():.2f}")
                
                # Add export buttons
                st.subheader("Dışa Aktarma")
                col1, col2 = st.columns(2)
                
                with col1:
                    try:
                        csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                        st.download_button(
                            label="CSV olarak indir",
                            data=csv,
                            file_name=f"sonuclar_{il}_{ilce}_{mahalle}_{ada}_{parsel}.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        logger.error(f"CSV export error: {str(e)}")
                        st.error("CSV dosyası oluşturulurken hata oluştu.")
                
                with col2:
                    try:
                        excel_data = export_to_excel(df)
                        st.download_button(
                            label="Excel olarak indir",
                            data=excel_data,
                            file_name=f"sonuclar_{il}_{ilce}_{mahalle}_{ada}_{parsel}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    except Exception as e:
                        logger.error(f"Excel export error: {str(e)}")
                        st.error("Excel dosyası oluşturulurken hata oluştu.")
            else:
                st.warning("Sonuç bulunamadı.")
        elif search_clicked:
            st.warning("Lütfen tüm alanları doldurun.")

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("Beklenmeyen bir hata oluştu. Lütfen sistem yöneticinize başvurun.")

if __name__ == "__main__":
    main()