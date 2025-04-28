import sys

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Rectangle
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
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

        # Initialize forces list
        self.forces = []  # List of tuples (magnitude, position)

        # Material properties
        self.materials = {
            # Metals
            "Aluminum": {"E": 69000, "poisson": 0.33, "density": 2700},  # MPa, kg/m^3
            "Steel": {"E": 200000, "poisson": 0.3, "density": 7850},
            "Stainless Steel": {"E": 193000, "poisson": 0.27, "density": 8000},
            "Brass": {"E": 105000, "poisson": 0.34, "density": 8500},
            "Copper": {"E": 117000, "poisson": 0.33, "density": 8960},
            "Titanium": {"E": 114000, "poisson": 0.34, "density": 4500},
            # Woods (average values, can vary significantly)
            "Oak": {"E": 11000, "poisson": 0.3, "density": 750},
            "Pine": {"E": 9000, "poisson": 0.3, "density": 550},
            "Maple": {"E": 10000, "poisson": 0.3, "density": 700},
            "Cedar": {"E": 7000, "poisson": 0.3, "density": 380},
            "Bamboo": {"E": 15000, "poisson": 0.3, "density": 600},
            # Plastics
            "PVC": {"E": 2800, "poisson": 0.38, "density": 1400},
            "HDPE": {"E": 800, "poisson": 0.46, "density": 970},
            "Polycarbonate": {"E": 2400, "poisson": 0.37, "density": 1200},
            "Nylon": {"E": 2000, "poisson": 0.4, "density": 1150},
            "ABS": {"E": 2000, "poisson": 0.35, "density": 1050},
            # Composites
            "GFRP": {
                "E": 25000,
                "poisson": 0.25,
                "density": 1800,
            },  # Glass Fiber Reinforced Plastic
            "CFRP": {
                "E": 150000,
                "poisson": 0.28,
                "density": 1600,
            },  # Carbon Fiber Reinforced Plastic
            # Other
            "Concrete": {"E": 30000, "poisson": 0.2, "density": 2400},
            "Glass": {"E": 70000, "poisson": 0.22, "density": 2500},
        }

        # Sort materials by category for the combo box
        self.material_categories = {
            "Metals": [
                "Aluminum",
                "Steel",
                "Stainless Steel",
                "Brass",
                "Copper",
                "Titanium",
            ],
            "Woods": ["Oak", "Pine", "Maple", "Cedar", "Bamboo"],
            "Plastics": ["PVC", "HDPE", "Polycarbonate", "Nylon", "ABS"],
            "Composites": ["GFRP", "CFRP"],
            "Other": ["Concrete", "Glass"],
        }

        # Default values
        self.default_dimension = "40"
        self.default_length = "1000"
        self.default_load = "3000"
        self.default_material = "Aluminum"

        # I-beam default values (mm)
        self.default_i_height = "100"
        self.default_i_width = "50"
        self.default_i_web = "5"
        self.default_i_flange = "8"

        # Rectangle default values (mm)
        self.default_rect_height = "80"
        self.default_rect_width = "40"

        # Tube default values (mm)
        self.default_tube_od = "60"
        self.default_tube_thickness = "3"

        # Square tube default values (mm)
        self.default_square_tube_od = "50"
        self.default_square_tube_thickness = "3"

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
        input_layout.addWidget(QLabel("Cross Section Type:"))
        self.section_group = QButtonGroup(self)
        self.square_radio = QRadioButton("Square")
        self.circular_radio = QRadioButton("Circular")
        self.i_beam_radio = QRadioButton("I-Beam")
        self.rect_radio = QRadioButton("Rectangle")
        self.tube_radio = QRadioButton("Circular Tube")
        self.square_tube_radio = QRadioButton("Square Tube")

        for radio in [
            self.square_radio,
            self.circular_radio,
            self.i_beam_radio,
            self.rect_radio,
            self.tube_radio,
            self.square_tube_radio,
        ]:
            self.section_group.addButton(radio)
            input_layout.addWidget(radio)
        self.square_radio.setChecked(True)

        # Create parameter input widgets
        # Square/Circle parameter
        self.simple_param_widget = QWidget()
        simple_layout = QVBoxLayout(self.simple_param_widget)
        self.dimension_label = QLabel("Side Length (mm):")
        self.dimension_input = QLineEdit(self.default_dimension)
        simple_layout.addWidget(self.dimension_label)
        simple_layout.addWidget(self.dimension_input)
        input_layout.addWidget(self.simple_param_widget)

        # I-beam parameters
        self.i_beam_widget = QWidget()
        i_beam_layout = QVBoxLayout(self.i_beam_widget)
        self.i_height_input = QLineEdit(self.default_i_height)
        self.i_width_input = QLineEdit(self.default_i_width)
        self.i_web_input = QLineEdit(self.default_i_web)
        self.i_flange_input = QLineEdit(self.default_i_flange)

        for label, widget in [
            ("Total Height (h) [mm]:", self.i_height_input),
            ("Flange Width (b) [mm]:", self.i_width_input),
            ("Web Thickness (tw) [mm]:", self.i_web_input),
            ("Flange Thickness (tf) [mm]:", self.i_flange_input),
        ]:
            i_beam_layout.addWidget(QLabel(label))
            i_beam_layout.addWidget(widget)

        self.i_beam_widget.hide()
        input_layout.addWidget(self.i_beam_widget)

        # Rectangle parameters
        self.rect_widget = QWidget()
        rect_layout = QVBoxLayout(self.rect_widget)
        self.rect_height_input = QLineEdit(self.default_rect_height)
        self.rect_width_input = QLineEdit(self.default_rect_width)

        for label, widget in [
            ("Height (h) [mm]:", self.rect_height_input),
            ("Width (b) [mm]:", self.rect_width_input),
        ]:
            rect_layout.addWidget(QLabel(label))
            rect_layout.addWidget(widget)

        self.rect_widget.hide()
        input_layout.addWidget(self.rect_widget)

        # Circular tube parameters
        self.tube_widget = QWidget()
        tube_layout = QVBoxLayout(self.tube_widget)
        self.tube_od_input = QLineEdit(self.default_tube_od)
        self.tube_thickness_input = QLineEdit(self.default_tube_thickness)

        for label, widget in [
            ("Outer Diameter (OD) [mm]:", self.tube_od_input),
            ("Wall Thickness (t) [mm]:", self.tube_thickness_input),
        ]:
            tube_layout.addWidget(QLabel(label))
            tube_layout.addWidget(widget)

        self.tube_widget.hide()
        input_layout.addWidget(self.tube_widget)

        # Square tube parameters
        self.square_tube_widget = QWidget()
        square_tube_layout = QVBoxLayout(self.square_tube_widget)
        self.square_tube_od_input = QLineEdit(self.default_square_tube_od)
        self.square_tube_thickness_input = QLineEdit(self.default_square_tube_thickness)

        for label, widget in [
            ("Outer Dimension (a) [mm]:", self.square_tube_od_input),
            ("Wall Thickness (t) [mm]:", self.square_tube_thickness_input),
        ]:
            square_tube_layout.addWidget(QLabel(label))
            square_tube_layout.addWidget(widget)

        self.square_tube_widget.hide()
        input_layout.addWidget(self.square_tube_widget)

        # Rest of the inputs
        input_layout.addWidget(QLabel("Beam Length (mm):"))
        self.length_input = QLineEdit(self.default_length)
        input_layout.addWidget(self.length_input)

        input_layout.addWidget(QLabel("Material:"))
        self.material_combo = QComboBox()

        # Add materials by category with separators
        for category, materials in self.material_categories.items():
            if self.material_combo.count() > 0:  # Add separator if not first category
                self.material_combo.addItem("─" * 20)  # Separator line
                self.material_combo.setItemData(
                    self.material_combo.count() - 1, 0, Qt.ItemDataRole.UserRole - 1
                )
            self.material_combo.addItem(f"== {category} ==")
            self.material_combo.setItemData(
                self.material_combo.count() - 1, 0, Qt.ItemDataRole.UserRole - 1
            )
            for material in materials:
                self.material_combo.addItem(material)

        self.material_combo.setCurrentText(self.default_material)
        self.material_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.material_combo.setMaxVisibleItems(15)  # Show more items in dropdown
        input_layout.addWidget(self.material_combo)

        # Material properties display with better formatting
        self.material_info = QLabel()
        self.material_info.setStyleSheet(
            """
            QLabel {
                font-size: 11pt;
                margin: 5px;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        """
        )
        input_layout.addWidget(self.material_info)

        # Support condition selection
        input_layout.addWidget(QLabel("Support Condition:"))
        self.support_group = QButtonGroup(self)
        self.single_support_radio = QRadioButton("Single Support (Cantilever)")
        self.both_ends_radio = QRadioButton("Both Ends Supported")
        self.single_support_radio.setChecked(True)

        for radio in [self.single_support_radio, self.both_ends_radio]:
            self.support_group.addButton(radio)
            input_layout.addWidget(radio)

        # Multiple forces section
        forces_label = QLabel("Forces")
        forces_label.setStyleSheet("font-size: 12pt; font-weight: bold; margin: 10px;")
        input_layout.addWidget(forces_label)

        # Force list
        self.force_list = QListWidget()
        self.force_list.setMaximumHeight(150)
        input_layout.addWidget(self.force_list)

        # Force input section
        force_input_widget = QWidget()
        force_input_layout = QHBoxLayout(force_input_widget)

        self.force_magnitude_input = QLineEdit()
        self.force_magnitude_input.setPlaceholderText("Force (N)")
        self.force_position_input = QLineEdit()
        self.force_position_input.setPlaceholderText("Position (mm)")

        force_input_layout.addWidget(QLabel("Force (N):"))
        force_input_layout.addWidget(self.force_magnitude_input)
        force_input_layout.addWidget(QLabel("Position (mm):"))
        force_input_layout.addWidget(self.force_position_input)

        input_layout.addWidget(force_input_widget)

        # Add/Remove force buttons
        force_buttons_widget = QWidget()
        force_buttons_layout = QHBoxLayout(force_buttons_widget)

        self.add_force_button = QPushButton("Add Force")
        self.remove_force_button = QPushButton("Remove Force")

        force_buttons_layout.addWidget(self.add_force_button)
        force_buttons_layout.addWidget(self.remove_force_button)

        input_layout.addWidget(force_buttons_widget)

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

        input_layout.addStretch()
        layout.addWidget(input_panel, stretch=1)

        # Create plots panel
        plots_panel = QWidget()
        plots_layout = QVBoxLayout(plots_panel)

        self.cross_section_figure = Figure(figsize=(6, 4))
        self.cross_section_canvas = FigureCanvas(self.cross_section_figure)
        self.deflection_figure = Figure(figsize=(6, 4))
        self.deflection_canvas = FigureCanvas(self.deflection_figure)

        plots_layout.addWidget(self.cross_section_canvas)
        plots_layout.addWidget(self.deflection_canvas)
        layout.addWidget(plots_panel, stretch=2)

        # Connect signals for instant updates
        self.section_group.buttonClicked.connect(self.on_section_change)
        self.dimension_input.textChanged.connect(self.on_input_change)
        self.length_input.textChanged.connect(self.on_input_change)
        self.material_combo.currentTextChanged.connect(self.on_material_change)

        # I-beam parameter connections
        self.i_height_input.textChanged.connect(self.on_input_change)
        self.i_width_input.textChanged.connect(self.on_input_change)
        self.i_web_input.textChanged.connect(self.on_input_change)
        self.i_flange_input.textChanged.connect(self.on_input_change)

        # Rectangle parameter connections
        self.rect_height_input.textChanged.connect(self.on_input_change)
        self.rect_width_input.textChanged.connect(self.on_input_change)

        # Circular tube parameter connections
        self.tube_od_input.textChanged.connect(self.on_input_change)
        self.tube_thickness_input.textChanged.connect(self.on_input_change)

        # Square tube parameter connections
        self.square_tube_od_input.textChanged.connect(self.on_input_change)
        self.square_tube_thickness_input.textChanged.connect(self.on_input_change)

        # Connect signals for force management
        self.add_force_button.clicked.connect(self.add_force)
        self.remove_force_button.clicked.connect(self.remove_force)
        self.support_group.buttonClicked.connect(self.on_input_change)

        # Initial updates
        self.update_material_info()
        self.calculate()

    def on_section_change(self):
        """Handle section type change"""
        self.simple_param_widget.hide()
        self.i_beam_widget.hide()
        self.rect_widget.hide()
        self.tube_widget.hide()
        self.square_tube_widget.hide()

        if self.square_radio.isChecked() or self.circular_radio.isChecked():
            self.simple_param_widget.show()
            self.dimension_label.setText(
                "Side Length (mm):"
                if self.square_radio.isChecked()
                else "Diameter (mm):"
            )
        elif self.i_beam_radio.isChecked():
            self.i_beam_widget.show()
        elif self.rect_radio.isChecked():
            self.rect_widget.show()
        elif self.tube_radio.isChecked():
            self.tube_widget.show()
        else:  # Square tube
            self.square_tube_widget.show()

        self.calculate()

    def calculate_section_properties(self):
        """Calculate area and moment of inertia based on section type"""
        if self.square_radio.isChecked():
            d = float(self.dimension_input.text())  # mm
            return d**2, d**4 / 12  # mm², mm⁴
        elif self.circular_radio.isChecked():
            d = float(self.dimension_input.text())  # mm
            r = d / 2
            return np.pi * r**2, np.pi * r**4 / 64  # mm², mm⁴
        elif self.i_beam_radio.isChecked():
            h = float(self.i_height_input.text())  # mm
            b = float(self.i_width_input.text())  # mm
            tw = float(self.i_web_input.text())  # mm
            tf = float(self.i_flange_input.text())  # mm

            # Area calculation
            A_web = tw * (h - 2 * tf)
            A_flanges = 2 * b * tf
            A = A_web + A_flanges

            # Moment of inertia calculation
            I_web = tw * (h - 2 * tf) ** 3 / 12
            I_flanges = 2 * (b * tf**3 / 12 + b * tf * ((h - tf) / 2) ** 2)
            I = I_web + I_flanges

            return A, I  # mm², mm⁴
        elif self.rect_radio.isChecked():
            h = float(self.rect_height_input.text())  # mm
            b = float(self.rect_width_input.text())  # mm
            return b * h, b * h**3 / 12  # mm², mm⁴
        elif self.tube_radio.isChecked():
            do = float(self.tube_od_input.text())  # mm
            t = float(self.tube_thickness_input.text())  # mm
            di = do - 2 * t
            ro = do / 2
            ri = di / 2
            A = np.pi * (ro**2 - ri**2)
            I = np.pi * (ro**4 - ri**4) / 4
            return A, I  # mm², mm⁴
        else:  # Square tube
            a = float(self.square_tube_od_input.text())  # mm
            t = float(self.square_tube_thickness_input.text())  # mm
            ai = a - 2 * t
            A = a**2 - ai**2
            I = (a**4 - ai**4) / 12
            return A, I  # mm², mm⁴

    def plot_cross_section(self, ax, dimension):
        """Plot cross section with annotations"""
        ax.clear()
        if self.square_radio.isChecked():
            d = float(self.dimension_input.text())
            patch = Rectangle(
                (-d / 2, -d / 2),
                d,
                d,
                fill=True,
                facecolor="lightblue",
                edgecolor="blue",
                alpha=0.7,
            )
            ax.add_patch(patch)

        elif self.circular_radio.isChecked():
            d = float(self.dimension_input.text())
            circle = Circle(
                (0, 0),
                d / 2,
                fill=True,
                facecolor="lightblue",
                edgecolor="blue",
                alpha=0.7,
            )
            ax.add_patch(circle)

        elif self.i_beam_radio.isChecked():
            h = float(self.i_height_input.text())
            b = float(self.i_width_input.text())
            tw = float(self.i_web_input.text())
            tf = float(self.i_flange_input.text())

            # Draw I-beam parts
            # Web
            ax.add_patch(
                Rectangle(
                    (-tw / 2, -h / 2),
                    tw,
                    h,
                    facecolor="lightblue",
                    edgecolor="blue",
                    alpha=0.7,
                )
            )
            # Top flange
            ax.add_patch(
                Rectangle(
                    (-b / 2, h / 2 - tf),
                    b,
                    tf,
                    facecolor="lightblue",
                    edgecolor="blue",
                    alpha=0.7,
                )
            )
            # Bottom flange
            ax.add_patch(
                Rectangle(
                    (-b / 2, -h / 2),
                    b,
                    tf,
                    facecolor="lightblue",
                    edgecolor="blue",
                    alpha=0.7,
                )
            )

        elif self.rect_radio.isChecked():
            h = float(self.rect_height_input.text())
            b = float(self.rect_width_input.text())
            patch = Rectangle(
                (-b / 2, -h / 2),
                b,
                h,
                fill=True,
                facecolor="lightblue",
                edgecolor="blue",
                alpha=0.7,
            )
            ax.add_patch(patch)

        elif self.tube_radio.isChecked():
            do = float(self.tube_od_input.text())
            t = float(self.tube_thickness_input.text())
            di = do - 2 * t
            # Outer circle
            circle_outer = Circle(
                (0, 0),
                do / 2,
                fill=True,
                facecolor="lightblue",
                edgecolor="blue",
                alpha=0.7,
            )
            # Inner circle (white to create hole)
            circle_inner = Circle(
                (0, 0),
                di / 2,
                fill=True,
                facecolor="white",
                edgecolor="blue",
                alpha=1.0,
            )
            ax.add_patch(circle_outer)
            ax.add_patch(circle_inner)

        else:  # Square tube
            a = float(self.square_tube_od_input.text())
            t = float(self.square_tube_thickness_input.text())
            ai = a - 2 * t
            # Outer square
            ax.add_patch(
                Rectangle(
                    (-a / 2, -a / 2),
                    a,
                    a,
                    fill=True,
                    facecolor="lightblue",
                    edgecolor="blue",
                    alpha=0.7,
                )
            )
            # Inner square (white to create hole)
            ax.add_patch(
                Rectangle(
                    (-ai / 2, -ai / 2),
                    ai,
                    ai,
                    fill=True,
                    facecolor="white",
                    edgecolor="blue",
                    alpha=1.0,
                )
            )

        # Set equal aspect ratio and limits
        max_dim = max(
            [
                float(
                    self.dimension_input.text()
                    if self.square_radio.isChecked() or self.circular_radio.isChecked()
                    else (
                        self.i_height_input.text()
                        if self.i_beam_radio.isChecked()
                        else self.rect_height_input.text()
                    )
                ),
                float(
                    self.i_width_input.text()
                    if self.i_beam_radio.isChecked()
                    else (
                        self.rect_width_input.text()
                        if self.rect_radio.isChecked()
                        else (
                            self.tube_od_input.text()
                            if self.tube_radio.isChecked()
                            else self.square_tube_od_input.text()
                        )
                    )
                ),
            ]
        )

        margin = max_dim * 0.2
        ax.set_xlim(-max_dim / 2 - margin, max_dim / 2 + margin)
        ax.set_ylim(-max_dim / 2 - margin, max_dim / 2 + margin)
        ax.set_aspect("equal")
        ax.grid(True)
        ax.set_title("Cross Section", pad=10, fontsize=14, fontweight="bold")
        ax.set_xlabel("mm", fontsize=10)
        ax.set_ylabel("mm", fontsize=10)

    def is_valid_input(self):
        """Validate all inputs"""
        try:
            if self.square_radio.isChecked() or self.circular_radio.isChecked():
                dimension = float(self.dimension_input.text())
                if dimension <= 0:
                    return False
            elif self.i_beam_radio.isChecked():
                h = float(self.i_height_input.text())
                b = float(self.i_width_input.text())
                tw = float(self.i_web_input.text())
                tf = float(self.i_flange_input.text())
                if any(x <= 0 for x in [h, b, tw, tf]) or tw > b or 2 * tf > h:
                    return False
            elif self.rect_radio.isChecked():
                h = float(self.rect_height_input.text())
                b = float(self.rect_width_input.text())
                if h <= 0 or b <= 0:
                    return False
            elif self.tube_radio.isChecked():
                do = float(self.tube_od_input.text())
                t = float(self.tube_thickness_input.text())
                if do <= 0 or t <= 0 or 2 * t >= do:
                    return False
            else:  # Square tube
                a = float(self.square_tube_od_input.text())
                t = float(self.square_tube_thickness_input.text())
                if a <= 0 or t <= 0 or 2 * t >= a:
                    return False

            length = float(self.length_input.text())
            return length > 0
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
            L = float(self.length_input.text())  # mm
            material = self.material_combo.currentText()
            E = self.materials[material]["E"]  # MPa
            density = self.materials[material]["density"]  # kg/m³

            # Calculate cross-sectional properties
            A, I = self.calculate_section_properties()  # mm², mm⁴

            # Calculate beam weight
            weight = density * A * L / 1e9  # kg (converting mm³ to m³)

            # Calculate deflection
            x = np.linspace(0, L, 100)
            y = self.calculate_deflection(x, L, E, I)
            max_deflection = np.max(np.abs(y))

            # Update results
            self.weight_label.setText(f"Beam Weight: {weight:.3f} kg")
            self.deflection_label.setText(
                f"Maximum Deflection: {max_deflection:.5f} mm"
            )

            # Plot cross section
            self.cross_section_figure.clear()
            ax = self.cross_section_figure.add_subplot(111)
            self.plot_cross_section(ax, None)
            self.cross_section_canvas.draw()

            # Plot deflection curve
            self.deflection_figure.clear()
            ax = self.deflection_figure.add_subplot(111)
            ax.plot(x, y, "b-", linewidth=2)

            # Set initial y-limits based on deflection
            y_max = max(abs(np.max(y)), abs(np.min(y)))
            ax.set_ylim(-y_max * 1.5, y_max * 1.5)

            # Plot force points and arrows
            for P, a in self.forces:
                # Plot force point
                ax.plot(a, 0, "ro", markersize=8)

                # Plot force arrow (smaller fixed length, direction matches force convention)
                arrow_length = y_max * 0.3  # 30% of max deflection
                if P < 0:  # Force points down (negative)
                    ax.annotate(
                        "",
                        xy=(a, 0),
                        xytext=(a, arrow_length),
                        arrowprops=dict(arrowstyle="->", color="red", lw=2),
                    )
                    ax.annotate(
                        f"{abs(P):.0f}N",
                        (a, arrow_length),
                        xytext=(10, 5),
                        textcoords="offset points",
                    )
                else:  # Force points up (positive)
                    ax.annotate(
                        "",
                        xy=(a, 0),
                        xytext=(a, -arrow_length),
                        arrowprops=dict(arrowstyle="->", color="red", lw=2),
                    )
                    ax.annotate(
                        f"{abs(P):.0f}N",
                        (a, -arrow_length),
                        xytext=(10, -20),
                        textcoords="offset points",
                    )

            # Plot support points
            if self.single_support_radio.isChecked():
                ax.plot(0, 0, "ks", markersize=10)
                ax.annotate(
                    "Support", (0, 0), xytext=(10, -20), textcoords="offset points"
                )
            else:
                ax.plot(0, 0, "ks", markersize=10)
                ax.plot(L, 0, "ks", markersize=10)
                ax.annotate(
                    "Support", (0, 0), xytext=(10, -20), textcoords="offset points"
                )
                ax.annotate(
                    "Support", (L, 0), xytext=(10, -20), textcoords="offset points"
                )

            ax.set_xlabel("Position along beam (mm)", fontsize=10)
            ax.set_ylabel("Deflection (mm)", fontsize=10)
            ax.set_title("Beam Deflection", pad=10, fontsize=14, fontweight="bold")
            ax.grid(True)
            ax.axhline(y=0, color="k", linestyle="--", alpha=0.3)
            self.deflection_canvas.draw()

        except ValueError:
            self.weight_label.setText("Error: Please check input values")
            self.deflection_label.setText("")

    def update_material_info(self):
        """Update material properties display with better formatting"""
        material = self.material_combo.currentText()
        if (
            material in self.materials
        ):  # Check if it's not a category header or separator
            props = self.materials[material]
            info = f"Material Properties for {material}:\n"
            info += f"Young's Modulus (E): {props['E']:,} MPa\n"
            info += f"Poisson's Ratio (ν): {props['poisson']:.2f}\n"
            info += f"Density (ρ): {props['density']:,} kg/m³"
            self.material_info.setText(info)
        else:
            self.material_info.setText("")

    def on_material_change(self):
        """Handle material change - update info and recalculate"""
        if (
            self.material_combo.currentText() in self.materials
        ):  # Only update if actual material selected
            self.update_material_info()
            self.calculate()

    def on_input_change(self):
        """Handle any input change"""
        self.calculate()

    def add_force(self):
        """Add a new force to the list"""
        try:
            magnitude = float(self.force_magnitude_input.text())
            position = float(self.force_position_input.text())
            L = float(self.length_input.text())

            if magnitude == 0 or position < 0 or position > L:
                return

            self.forces.append((magnitude, position))
            sign = "+" if magnitude > 0 else "-" if magnitude < 0 else ""
            self.force_list.addItem(
                f"Force: {sign}{abs(magnitude):.1f} N at {position:.1f} mm"
            )

            # Clear inputs
            self.force_magnitude_input.clear()
            self.force_position_input.clear()

            self.calculate()

        except ValueError:
            pass

    def remove_force(self):
        """Remove selected force from the list"""
        current_row = self.force_list.currentRow()
        if current_row >= 0:
            self.force_list.takeItem(current_row)
            self.forces.pop(current_row)
            self.calculate()

    def calculate_deflection(self, x, L, E, I):
        """Calculate deflection at point x considering all forces and support conditions
        Sign convention: positive forces point upward, negative forces point downward
        Positive deflection is upward"""
        if not self.forces:
            return np.zeros_like(x)
        y = np.zeros_like(x)
        if self.single_support_radio.isChecked():
            # Cantilever beam with multiple forces
            for P, a in self.forces:
                # Negative P causes downward deflection
                mask_before = x <= a
                y[mask_before] += (
                    P * x[mask_before] ** 2 * (3 * a - x[mask_before])
                ) / (6 * E * I)
                mask_after = x > a
                y[mask_after] += (P * a**2 * (3 * x[mask_after] - a)) / (6 * E * I)
        else:
            # Simply supported beam with multiple forces (correct superposition)
            for P, a in self.forces:
                # Negative P causes downward deflection
                b = L - a
                mask_before = x < a
                mask_after = x >= a
                # For x < a
                y[mask_before] += (
                    P * b * x[mask_before] * (L**2 - b**2 - x[mask_before] ** 2)
                ) / (6 * E * I * L)
                # For x >= a
                y[mask_after] += (
                    P
                    * a
                    * (L - x[mask_after])
                    * (2 * L * x[mask_after] - x[mask_after] ** 2 - a**2)
                ) / (6 * E * I * L)
        return y


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeamDeflectionCalculator()
    window.show()
    sys.exit(app.exec())
