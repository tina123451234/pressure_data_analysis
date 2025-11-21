import streamlit as st
import pandas as pd

class PressureDataGUI:
    def __init__(self):
        # Initialize session state variables (replacing instance variables)
        if 'csv_path' not in st.session_state:
            st.session_state.csv_path = None
        if 'xsl_path' not in st.session_state:
            st.session_state.xsl_path = None
        if 'merged_data' not in st.session_state:
            st.session_state.merged_data = None
        if 'columns' not in st.session_state:
            st.session_state.columns = []
        if 'pressure_channel' not in st.session_state:
            st.session_state.pressure_channel = None
        if 'status' not in st.session_state:
            st.session_state.status = "Ready"
    
    def create_widgets(self):
        """Create all GUI elements"""
        # Title
        st.title("Pressure Data Analysis Tool")
        
        # File selection section
        st.subheader("File Selection")
        
        # CSV file selection
        csv_file = st.file_uploader("Select CSV File", type=['csv'], key='csv_uploader')
        if csv_file is not None:
            self.select_csv(csv_file)
        
        # XSL file selection
        xsl_file = st.file_uploader("Select XSL File", type=['xsl', 'xlsx'], key='xsl_uploader')
        if xsl_file is not None:
            self.select_xsl(xsl_file)
        
        # Pressure channel input
        st.session_state.pressure_channel = st.text_input(
            "Pressure Channel:", 
            value=st.session_state.pressure_channel or "1"
        )
        
        # Separator
        st.markdown("---")
        
        # Action buttons
        st.subheader("Actions")
        
        # Merge button
        if st.button("Merge Files", use_container_width=True):
            self.merge_files()
        
        # Plot configuration section
        st.markdown("---")
        st.subheader("Plot Configuration")
        
        # X-axis and Y-axis selection
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis_options = st.session_state.columns if st.session_state.columns else [""]
            x_axis_disabled = len(st.session_state.columns) == 0
            x_axis = st.selectbox(
                "X-Axis:",
                options=x_axis_options,
                disabled=x_axis_disabled,
                key='x_axis_select'
            )
        
        with col2:
            y_axis_options = st.session_state.columns if st.session_state.columns else [""]
            y_axis_disabled = len(st.session_state.columns) == 0
            y_axis = st.selectbox(
                "Y-Axis:",
                options=y_axis_options,
                index=min(1, len(y_axis_options) - 1) if len(y_axis_options) > 0 else 0,
                disabled=y_axis_disabled,
                key='y_axis_select'
            )
        
        # Create Plot button
        plot_disabled = st.session_state.merged_data is None
        if st.button("Create Plot", disabled=plot_disabled, use_container_width=True, type="primary"):
            self.create_plot(x_axis, y_axis)
        
        # Status bar
        st.caption(f"Status: {st.session_state.status}")
    
    def select_csv(self, file):
        """Handle CSV file selection"""
        st.session_state.csv_path = file
        self.update_status("CSV file selected")
        self.load_columns()
    
    def select_xsl(self, file):
        """Handle XSL file selection"""
        st.session_state.xsl_path = file
        self.update_status("XSL file selected")
        self.load_columns()
    
    def load_columns(self):
        """Load columns from files after merge or when both files are selected"""
        # This will be called after merge, or we can try to preview columns from raw files
        # For now, we'll enable it only after merge
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
    
    def populate_dropdowns(self, columns):
        """Populate the axis dropdowns with column names"""
        st.session_state.columns = columns
    
    def merge_files(self):
        """Call merge files method"""
        if not self.check_files_selected():
            return
        
        # Get pressure channel input
        pressure_channel = st.session_state.pressure_channel.strip()
        if not pressure_channel:
            st.warning("Missing Pressure Channel: Please enter a pressure channel value.")
            return
        
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
            
            self.update_status("Merge complete! Select axes for plotting.")
            st.success(f"Success: Files merged successfully!\nPressure Channel: {pressure_channel}\n{len(columns)} columns available for plotting.")
            
        except Exception as e:
            self.update_status("Error occurred")
            st.error(f"Error: An error occurred:\n{str(e)}")
    
    def create_plot(self, x_col, y_col):
        """Create plot with selected axes"""
        if st.session_state.merged_data is None:
            st.warning("No Data: Please merge files first before creating a plot.")
            return
        
        if not x_col or not y_col:
            st.warning("Missing Selection: Please select both X and Y axes.")
            return
        
        if x_col == y_col:
            st.warning("Invalid Selection: X and Y axes must be different columns.")
            return
        
        try:
            self.update_status(f"Creating plot: {x_col} vs {y_col}...")
            
            # TODO: Replace with your actual plot function
            # from plotting import create_plot
            # create_plot(st.session_state.merged_data, x_col, y_col)
            
            # Placeholder
            st.write(f"Creating plot with X={x_col}, Y={y_col}")
            st.write(f"Data shape: {st.session_state.merged_data.shape}")
            
            self.update_status(f"Plot complete: {x_col} vs {y_col}")
            st.success(f"Success: Plot created successfully!\nX: {x_col}\nY: {y_col}")
            
        except Exception as e:
            self.update_status("Error occurred")
            st.error(f"Error: An error occurred:\n{str(e)}")


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