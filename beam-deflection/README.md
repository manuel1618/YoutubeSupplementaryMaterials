# Beam Deflection Calculator

An interactive tool for calculating and visualizing beam deflection under tip loading conditions.

## Features

- Choose between square and circular cross-sections
- Input beam dimensions in millimeters
- Select material (Aluminum or Steel) with automatic property loading
- Calculate beam weight and tip deflection
- Real-time visualization of:
  - Beam deflection curve
  - Cross-section shape

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python beam_deflection.py
```

2. Input the required parameters:
   - Select cross-section type (Square or Circular)
   - Enter dimension (side length for square, diameter for circular) in mm
   - Enter beam length in mm
   - Select material (Aluminum or Steel)
   - Enter tip load in Newtons

3. Click "Calculate" to see results:
   - Beam weight in Newtons
   - Tip deflection in millimeters
   - Visualization of deflection curve
   - Visualization of cross-section

## Technical Details

- Material Properties:
  - Aluminum: E = 69,000 MPa, ν = 0.33, ρ = 2,700 kg/m³
  - Steel: E = 200,000 MPa, ν = 0.3, ρ = 7,850 kg/m³
- All calculations use SI units internally
- Deflection calculated using beam theory 