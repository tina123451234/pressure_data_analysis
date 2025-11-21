import streamlit as st
import pandas as pd

class PressureDataGUI:
    def __init__(self):
        # Initialize session state variables
        if 'csv_path' not in st.session_state:
            st.session_state.csv_path = None
        if 'xsl_path' not in st.session_state:
            st.session_state.xsl_path = None
        if 'merged_data' not in st.session_state:
            st.session_state.merged_data = None
        if 'columns' not in st.session_state:
            st.session_state.columns = []
        if 'pressure_channel' not in st.session_state:
            st.session_state.pressure_channel = "1"
        if 'status' not in st.session_state:
            st.session_state.status = "Ready"
        if 'csv_filename' not in st.session_state:
            st.session_state.csv_filename = "No file selected"
        if 'xsl_filename' not in st.session_state:
            st.session_state.xsl_filename = "No file selected"
    
    def create_widgets(self):
        """Create all GUI elements"""
        # Title
        st.markdown("<h1 style='text-align: center;'>Pressure Data Analysis Tool</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # File selection section
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Select CSV File", use_container_width=True, key='csv_button'):
                pass  # Button styling only
        with col2:
            st.markdown(f"<p style='color: gray; padding-top: 8px;'>{st.session_state.csv_filename}</p>", unsafe_allow_html=True)
        
        csv_file = st.file_uploader("", type=['csv'], key='csv_uploader', label_visibility='collapsed')
        if csv_file is not None:
            self.select_csv(csv_file)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Select XSL File", use_container_width=True, key='xsl_button'):
                pass  # Button styling only
        with col2:
            st.markdown(f"<p style='color: gray; padding-top: 8px;'>{st.session_state.xsl_filename}</p>", unsafe_allow_html=True)
        
        xsl_file = st.file_uploader("", type=['xsl', 'xlsx'], key='xsl_uploader', label_visibility='collapsed')
        if xsl_file is not None:
            self.select_xsl(xsl_file)
        
        # Separator
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Actions section
        st.markdown("<h2 style='text-align: center;'>Actions</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the buttons with columns
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("Merge Files", use_container_width=True, key='merge_button'):
                self.merge_files()
            
            if st.button("Create Plot Type 1", use_container_width=True, key='plot1_button'):
                self.create_plot_type(1)
            
            if st.button("Create Plot Type 2", use_container_width=True, key='plot2_button'):
                self.create_plot_type(2)
            
            if st.button("Create Plot Type 3", use_container_width=True, key='plot3_button'):
                self.create_plot_type(3)
            
            if st.button("Create Plot Type 4", use_container_width=True, key='plot4_button'):
                self.create_plot_type(4)
        
        # Status bar at bottom
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"<div style='background-color: lightgray; padding: 10px; position: fixed; bottom: 0; left: 0; width: 100%;'>Status: {st.session_state.status}</div>", unsafe_allow_html=True)
    
    def select_csv(self, file):
        """Handle CSV file selection"""
        st.session_state.csv_path = file
        st.session_state.csv_filename = file.name
        self.update_status("CSV file selected")
        self.load_columns()
    
    def select_xsl(self, file):
        """Handle XSL file selection"""
        st.session_state.xsl_path = file
        st.session_state.xsl_filename = file.name
        self.update_status("XSL file selected")
        self.load_columns()
    
    def load_columns(self):
        """Load columns from files after merge or when both files are selected"""
        pass
    
    def check_files_selected(self):
        """Check if both files are selected"""
        if not st.session_state.csv_path or not st.session_state.xsl_path:
            st.warning("Missing Files: Please select both CSV and XSL files before proceeding.")
            return False
        return True
    
    def update_status(self, message):
        """Update status bar message"""
        st.session_state.status = message
        st.rerun()
    
    def populate_dropdowns(self, columns):
        """Populate the axis dropdowns with column names"""
        st.session_state.columns = columns
    
    def merge_files(self):
        """Call merge files method"""
        if not self.check_files_selected():
            return
        
        # Get pressure channel input (default to "1" if not specified)
        pressure_channel = st.session_state.pressure_channel
        
        try:
            self.update_status("Merging files...")
            
            # TODO: Replace with your actual merge function
            # from merge import merge_files
            # st.session_state.merged_data = merge_files(
            #     st.session_state.csv_path, 
            #     st.session_state.xsl_path, 
            #     pressure_channel
            # )
            
            # Placeholder - Load CSV to get columns (temporary)
            st.session_state.merged_data = pd.read_csv(st.session_state.csv_path)
            
            # Get column names and populate dropdowns
            columns = list(st.session_state.merged_data.columns)
            self.populate_dropdowns(columns)
            
            self.update_status("Merge complete!")
            st.success(f"Files merged successfully! {len(columns)} columns available.")
            
        except Exception as e:
            self.update_status("Error occurred")
            st.error(f"Error: {str(e)}")
    
    def create_plot_type(self, plot_type):
        """Create plot based on plot type"""
        if st.session_state.merged_data is None:
            st.warning("No Data: Please merge files first before creating a plot.")
            return
        
        try:
            self.update_status(f"Creating Plot Type {plot_type}...")
            
            # TODO: Replace with your actual plot functions
            # from plotting import create_plot_type_1, create_plot_type_2, etc.
            # if plot_type == 1:
            #     create_plot_type_1(st.session_state.merged_data)
            # elif plot_type == 2:
            #     create_plot_type_2(st.session_state.merged_data)
            # elif plot_type == 3:
            #     create_plot_type_3(st.session_state.merged_data)
            # elif plot_type == 4:
            #     create_plot_type_4(st.session_state.merged_data)
            
            # Placeholder
            st.write(f"Creating Plot Type {plot_type}")
            st.write(f"Data shape: {st.session_state.merged_data.shape}")
            
            self.update_status(f"Plot Type {plot_type} complete!")
            st.success(f"Plot Type {plot_type} created successfully!")
            
        except Exception as e:
            self.update_status("Error occurred")
            st.error(f"Error: {str(e)}")


def main():
    st.set_page_config(
        page_title="Pressure Data Analysis Tool",
        page_icon="📊",
        layout="centered"
    )
    
    app = PressureDataGUI()
    app.create_widgets()


if __name__ == "__main__":
    main()