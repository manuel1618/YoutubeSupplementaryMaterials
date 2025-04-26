import sys

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Rectangle
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class BeamDeflectionCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beam Deflection Calculator")
        self.setGeometry(100, 100, 1200, 800)

        # Material properties
        self.materials = {
            "Aluminum": {"E": 69000, "poisson": 0.33, "density": 2700},  # MPa  # kg/m^3
            "Steel": {"E": 200000, "poisson": 0.3, "density": 7850},  # MPa  # kg/m^3
        }

        # Default values
        self.default_dimension = "40"
        self.default_length = "1000"
        self.default_load = "3000"
        self.default_material = "Aluminum"
        self.default_cross_section = "Square"

        self.init_ui()

    def init_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Create input panel
        input_panel = QWidget()
        input_layout = QVBoxLayout(input_panel)

        # Title for input panel
        title_label = QLabel("Input Parameters")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold; margin: 10px;")
        input_layout.addWidget(title_label)

        # Cross section selection
        cross_section_group = QButtonGroup(self)
        self.square_radio = QRadioButton("Square")
        self.circular_radio = QRadioButton("Circular")
        cross_section_group.addButton(self.square_radio)
        cross_section_group.addButton(self.circular_radio)
        self.square_radio.setChecked(True)

        input_layout.addWidget(QLabel("Cross Section Type:"))
        input_layout.addWidget(self.square_radio)
        input_layout.addWidget(self.circular_radio)

        # Dimension input
        self.dimension_label = QLabel("Side Length (mm):")
        self.dimension_input = QLineEdit(self.default_dimension)
        input_layout.addWidget(self.dimension_label)
        input_layout.addWidget(self.dimension_input)

        # Beam length input
        input_layout.addWidget(QLabel("Beam Length (mm):"))
        self.length_input = QLineEdit(self.default_length)
        input_layout.addWidget(self.length_input)

        # Material selection
        input_layout.addWidget(QLabel("Material:"))
        self.material_combo = QComboBox()
        self.material_combo.addItems(["Aluminum", "Steel"])
        self.material_combo.setCurrentText(self.default_material)
        input_layout.addWidget(self.material_combo)

        # Material properties display
        self.material_info = QLabel()
        self.material_info.setStyleSheet("font-size: 11pt; margin: 5px;")
        input_layout.addWidget(self.material_info)

        # Load input
        input_layout.addWidget(QLabel("Tip Load (N):"))
        self.load_input = QLineEdit(self.default_load)
        input_layout.addWidget(self.load_input)

        # Results display
        results_label = QLabel("Results")
        results_label.setStyleSheet("font-size: 14pt; font-weight: bold; margin: 10px;")
        input_layout.addWidget(results_label)

        self.weight_label = QLabel("Beam Weight: ")
        self.deflection_label = QLabel("Tip Deflection: ")
        self.weight_label.setStyleSheet("font-size: 11pt; margin: 5px;")
        self.deflection_label.setStyleSheet("font-size: 11pt; margin: 5px;")
        input_layout.addWidget(self.weight_label)
        input_layout.addWidget(self.deflection_label)

        # Add spacer at the bottom of input panel
        input_layout.addStretch()

        # Add input panel to main layout
        layout.addWidget(input_panel, stretch=1)

        # Create plots panel
        plots_panel = QWidget()
        plots_layout = QVBoxLayout(plots_panel)

        # Create matplotlib figures
        self.cross_section_figure = Figure(figsize=(6, 4))
        self.cross_section_canvas = FigureCanvas(self.cross_section_figure)
        self.deflection_figure = Figure(figsize=(6, 4))
        self.deflection_canvas = FigureCanvas(self.deflection_figure)

        plots_layout.addWidget(self.cross_section_canvas)
        plots_layout.addWidget(self.deflection_canvas)

        # Add plots panel to main layout
        layout.addWidget(plots_panel, stretch=2)

        # Connect signals for instant updates
        self.square_radio.toggled.connect(self.on_input_change)
        self.circular_radio.toggled.connect(self.on_input_change)
        self.dimension_input.textChanged.connect(self.on_input_change)
        self.length_input.textChanged.connect(self.on_input_change)
        self.load_input.textChanged.connect(self.on_input_change)
        self.material_combo.currentTextChanged.connect(self.on_material_change)

        # Initial updates
        self.update_material_info()
        self.update_dimension_label()
        self.calculate()  # Initial calculation with default values

    def update_dimension_label(self):
        if self.square_radio.isChecked():
            self.dimension_label.setText("Side Length (mm):")
        else:
            self.dimension_label.setText("Diameter (mm):")

    def update_material_info(self):
        material = self.material_combo.currentText()
        props = self.materials[material]
        info = f"E: {props['E']} MPa\n"
        info += f"Poisson's Ratio: {props['poisson']}\n"
        info += f"Density: {props['density']} kg/m³"
        self.material_info.setText(info)

    def on_material_change(self):
        """Handle material change - update info and recalculate"""
        self.update_material_info()
        self.calculate()

    def on_input_change(self):
        """Handle any input change"""
        self.calculate()

    def is_valid_input(self):
        """Validate all inputs"""
        try:
            dimension = float(self.dimension_input.text())
            length = float(self.length_input.text())
            load = float(self.load_input.text())
            return dimension > 0 and length > 0 and load >= 0
        except ValueError:
            return False

    def calculate(self):
        """Calculate and update display"""
        if not self.is_valid_input():
            self.weight_label.setText("Error: Please check input values")
            self.deflection_label.setText("")
            return

        try:
            # Get inputs
            L = float(self.length_input.text()) / 1000  # Convert mm to m
            P = float(self.load_input.text())  # Load in N
            dimension = float(self.dimension_input.text()) / 1000  # Convert mm to m
            material = self.material_combo.currentText()
            E = self.materials[material]["E"] * 1e6  # Convert MPa to Pa
            density = self.materials[material]["density"]

            # Calculate cross-sectional properties
            if self.square_radio.isChecked():
                A = dimension**2
                I = (dimension**4) / 12
            else:
                r = dimension / 2
                A = np.pi * r**2
                I = (np.pi * r**4) / 64

            # Calculate beam weight
            weight = density * A * L  # kg

            # Calculate deflection
            x = np.linspace(0, L, 100)
            y = -(P * x**2 * (3 * L - x)) / (6 * E * I)
            max_deflection = (P * L**3) / (3 * E * I)

            # Update results
            self.weight_label.setText(f"Beam Weight: {weight:.3f} kg")
            self.deflection_label.setText(
                f"Tip Deflection: {max_deflection*1000:.5f} mm"
            )

            # Plot cross section
            self.cross_section_figure.clear()
            ax = self.cross_section_figure.add_subplot(111)
            if self.square_radio.isChecked():
                ax.add_patch(
                    Rectangle(
                        (-dimension / 2 * 1000, -dimension / 2 * 1000),
                        dimension * 1000,
                        dimension * 1000,
                        fill=True,
                        facecolor="lightblue",
                        edgecolor="blue",
                        alpha=0.7,
                    )
                )
            else:
                circle = Circle(
                    (0, 0),
                    dimension / 2 * 1000,
                    fill=True,
                    facecolor="lightblue",
                    edgecolor="blue",
                    alpha=0.7,
                )
                ax.add_patch(circle)

            ax.set_aspect("equal")
            ax.set_xlim(-dimension * 1000, dimension * 1000)
            ax.set_ylim(-dimension * 1000, dimension * 1000)
            ax.grid(True)
            title = ax.set_title(
                "Cross Section", pad=10, fontsize=14, fontweight="bold"
            )
            ax.set_xlabel("mm", fontsize=10)
            ax.set_ylabel("mm", fontsize=10)
            self.cross_section_canvas.draw()

            # Plot deflection curve
            self.deflection_figure.clear()
            ax = self.deflection_figure.add_subplot(111)
            ax.plot(x * 1000, y * 1000, "b-", linewidth=2)
            ax.set_xlabel("Position along beam (mm)", fontsize=10)
            ax.set_ylabel("Deflection (mm)", fontsize=10)
            title = ax.set_title(
                "Beam Deflection", pad=10, fontsize=14, fontweight="bold"
            )
            ax.grid(True)
            ax.axhline(y=0, color="k", linestyle="--", alpha=0.3)
            self.deflection_canvas.draw()

        except ValueError:
            self.weight_label.setText("Error: Please check input values")
            self.deflection_label.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeamDeflectionCalculator()
    window.show()
    sys.exit(app.exec())
