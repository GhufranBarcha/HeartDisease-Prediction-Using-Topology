
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from gtda.time_series import SingleTakensEmbedding
from gtda.homology import VietorisRipsPersistence
from gtda.plotting import plot_point_cloud
import plotly.graph_objects as go
import plotly.io as pio
import base64


# st.set_page_config(page_title=" Topology Heart Disease",page_icon="🚑" , layout="wide") # For other ui uncomment this
st.set_page_config(page_title=" Topology Heart Disease",page_icon="🚑" , layout="centered")

pio.templates.default = "plotly_white"
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
col11 ,col22 = st.columns([1,9])
with col22:
     st.title("Cardiac Arrhythmia Detection")

## Required for prediction
def embedder(y_list1):
        embedding_dimension_periodic = 3
        embedding_time_delay_periodic = 8
        stride = 10

        embedder_periodic = SingleTakensEmbedding(
            parameters_type="fixed",
            n_jobs=2,
            time_delay=embedding_time_delay_periodic,
            dimension=embedding_dimension_periodic,
            stride=stride,
        )

        y_periodic_embedded = embedder_periodic.fit_transform(y_list1)
        msg = f"Shape of embedded time series: {y_periodic_embedded.shape}"
        return y_periodic_embedded, msg   
    
selected = option_menu(
        menu_title=None,
        options= ["Project Info","Code" ,"Patient Prediction","Research Paper"],
        icons = ["icon bi-house" ,"filetype-py" ,"file-earmark-excel","filetype-pdf"],
        default_index=0,
        orientation="horizontal",
        styles={
                    "nav-link-selected": {"font-weight": "normal", "background": "linear-gradient(to right, red, orange)"},
                    "nav-link-selected": {"font-weight": "normal", "background": "#0066FF"},
                    "nav-link": {"display": "inline-block", "margin-right": "auto"},
                    "icon": {"display": "block", "margin-bottom": "5px"}
                    }   

    )
    
if selected == "Project Info":
        
        st.markdown(""" 
                    # Welcome to our Topological Data Analysis Project

Are you curious about the fascinating world of algebraic topology and its practical applications? You're in the right place! 

## About Our Project

**Algebraic topology** is a powerful tool with a wide range of applications, from oncology and 3D shape segmentation to gravitational wave detection and handwritten digit classification. In our project, we dive deep into the applications of **persistent homology** and **simplicial complexes**, particularly the **Vietoris Rips Complex**.

## Our Mission

We aim to use these mathematical tools to model **ECG data** from patients suffering from **Ventricular Tachycardia**. This condition causes the heart's ventricles to beat abnormally quickly. By comparing the results with data from healthy individuals, we're shedding light on the differences between **persistence diagrams** and **persistence images** generated from this homology analysis.

## Why It Matters

Our project isn't just about mathematics and data analysis; it has real-world implications. The power of **topological data analysis** lies in its ability to reveal essential information hidden within complex datasets. In an age of big data, we must find innovative ways to extract valuable insights without losing crucial details.

## Impact on Society

Understanding Ventricular Tachycardia is crucial for the medical field. It can lead to life-threatening situations if left untreated, such as cardiac arrest or heart attack. With our research, we hope to contribute to the early detection and proper treatment of this condition, potentially saving lives.

## Join Us on This Journey

Follow along as we explore the topological features of ECG data and discover new insights. Whether you're a data enthusiast, a medical professional, or just someone curious about the intersection of mathematics and healthcare, there's something here for everyone.

Stay tuned for our findings, results, and future work. Together, we can make a difference!


                    """)
      
    
    
    
#Code markdown   
if selected == "Code":
        st.markdown("""
                       
               ## Prediction Code

Here, we present the code used for prediction and analysis based on the ECG data. This code includes the generation of a time series embedding and persistence diagram for the first patient with Ventricular Tachycardia. 

```python
from gtda.time_series import SingleTakensEmbedding

# Define parameters
embedding_dimension_periodic = 3
embedding_time_delay_periodic = 8
stride = 10

# Create the embedder
embedder_periodic = SingleTakensEmbedding(
    parameters_type="fixed",
    n_jobs=2,
    time_delay=embedding_time_delay_periodic,
    dimension=embedding_dimension_periodic,
    stride=stride,
)

# Fit and transform the data
y_periodic_embedded = embedder_periodic.fit_transform(y_list1)

# Print the shape of the embedded time series
print(f"Shape of embedded time series: {y_periodic_embedded.shape}")

# Plot point cloud
from gtda.plotting import plot_point_cloud
plot_point_cloud(y_periodic_embedded)

# Generate the persistence diagram for the first patient with Ventricular Tachycardia
y_periodic_embedded = y_periodic_embedded[None, :, :]

# Define homology dimensions
homology_dimensions = [0, 1, 2]

# Create the Vietoris-Rips persistence object
from gtda.homology import VietorisRipsPersistence
periodic_persistence = VietorisRipsPersistence(
    homology_dimensions=homology_dimensions,
    n_jobs=6
)

# Print a message
print("Persistence diagram for periodic signal")

# Fit and transform, then plot the persistence diagram
periodic_persistence.fit_transform_plot(y_periodic_embedded)

# Create the Vietoris-Rips persistence object for nonperiodic signal
nonperiodic_persistence = VietorisRipsPersistence(
    homology_dimensions=homology_dimensions,
    n_jobs=6
)

# Print a message
print("Persistence diagram for nonperiodic signal")

# Fit and transform, then plot the persistence diagram for nonperiodic signal
nonperiodic_persistence.fit_transform_plot(y_nonperiodic_embedded)

                    """)
        
        
    
    
    
    


## Prediction code    
if selected == "Patient Prediction":
    

    
    def main():
        st.markdown(" ### Detection using Excel file")
        st.write("Upload a csv or excel file for prediction")
        
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx","csv"])
        try:
            if uploaded_file is not None:
                df = pd.read_excel(uploaded_file)
                filename = uploaded_file.name
                if ".xlsx" in filename:
                    fnum = filename.index(".xlsx")
                    filename = filename[:fnum]
                if ".csv" in filename:
                    fnum = filename.index(".csv")
                    filename = filename[:fnum]    
                

                # Plot ECG
                y_list1 = df["ECG"].tolist()
                x_list = list(range(0, 4797, 4))
                fig = go.Figure(data=go.Scatter(x=x_list, y=y_list1))
                fig.update_layout(
                    xaxis_title="Time (milliseconds)", 
                    yaxis_title="Electric Signal(millivolts)",
                    
                    title = f"  Time Series Data graph of {filename}",
                    title_x = 0.2,
                    title_font_size=18
                )
                st.plotly_chart(fig ,use_container_width=True)

                # 3D plot 
                y_periodic_embedded, msg = embedder(y_list1)
                st.write(f"**{msg}**")    
                plot1 = plot_point_cloud(y_periodic_embedded)
                st.plotly_chart(plot1,use_container_width=True)

                # Persistence diagrams
                y_periodic_embedded = y_periodic_embedded[None, :, :]
                homology_dimensions = [0, 1]  
                periodic_persistence = VietorisRipsPersistence(homology_dimensions=homology_dimensions, n_jobs=6)
                d = periodic_persistence.fit_transform(y_periodic_embedded)
                
            
                st.write(f"""
                        ### Persistence diagram for periodic signal for {filename}
                        """)
                st.plotly_chart(periodic_persistence.plot(d) ,use_container_width=True ,template = "plotly_dark")
                
                
                
                nonperiodic_persistence = VietorisRipsPersistence(homology_dimensions=homology_dimensions, n_jobs=6) 
                n = nonperiodic_persistence.fit_transform(y_periodic_embedded)
                
                st.write(f"""
                        ### Persistence diagram for nonperiodic signal for {filename}
                        """)
                st.plotly_chart(nonperiodic_persistence.plot(n) ,use_container_width=True)

        except Exception as e:
            st.warning('Something went Wrong. please upload file Again', icon="⚠️")
            st.write(e)
            

    if __name__ == "__main__":
        main()
    
    
    
    
if selected == "Research Paper":
    
        col1, col2 ,col3= st.columns([1,8,1])
        col2.markdown("### Read and Download the Paper here.")
        with col2:



                      
        
            def show_pdf(file_path):
                with open(file_path,"rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    # st.markdown("""
                    #          <embed src="https://thomasmorestudies.org/wp-content/uploads/2020/09/Richard.pdf" width="800" height="800">
                    #      """, unsafe_allow_html=True)    
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)    
            show_pdf('Applications_of_Topology_to_the_Detection_of_Ventricular_Tachycardia_Zhang_Tumuluri.pdf')
            

