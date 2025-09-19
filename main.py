# https://idseditor.solibri.com/ids-editor
# https://docs.ifcopenshell.org/ifctester.html
# https://github.com/IfcOpenShell/IfcOpenShell
# https://github.com/IfcOpenShell/IfcOpenShell/tree/v0.8.0/src/ifctester



import os
import webbrowser
import ifcopenshell
from ifctester import ids, reporter

# Load IFC file and extract its filename


filepath = r"ADD_PATH"
my_ifc = ifcopenshell.open(filepath)
file_name = filepath.split("\\")[-1]
# Create new IDS
specs = ids.Ids(title="""My IDS
                %s""" % file_name, 
                copyright="luca.moretti@anex.ch",
                version="V1.0",
                description="""BESCHREIBUNG""",
                author="Luca Moretti",
                date="17.09.2025",
                purpose="Modellprüfung",
                milestone="Abgabe")

# add specification to it


## globale requirements
req_dia = ids.Property(
    baseName="Durchmesser DN",
    propertySet="Pset_ANEX",
    value=ids.Restriction(base="number"),
    dataType="IfcLengthMeasure", #IfcText, IfcBoolean, IfcLengthMeasure
    instructions="'Durchmesser DN' muss im PropertySet 'Pset_ANEX' vorhanden sein und einen numerischen Wert haben.",
    cardinality="required")

req_len = ids.Property(
    baseName="Länge",
    propertySet="Pset_ANEX",
    value=ids.Restriction(base="number"),
    dataType="IfcLengthMeasure", #IfcText, IfcBoolean, IfcLengthMeasure
    instructions="'Länge' muss einen numerischen Wert haben.",
    cardinality="required")

req_tag = ids.Property(
    baseName="Kennzeichen",
    value=ids.Restriction(base="string",options={"pattern": r"^[A-Z]\d{2}-[A-Z]{2}\d{3}$"}),
    propertySet="Pset_ANEX",
    dataType="IfcText", #IfcText, IfcBoolean, IfcLengthMeasure
    instructions="'Kennzeichen' muss definiert sein",
    cardinality="required")

req_anl = ids.Property(
    baseName="Anlage",
    value=ids.Restriction(base="string",options={"pattern": r"^[A-Z]\d{2}$"}),
    propertySet="Pset_ANEX",
    dataType="IfcText", #IfcText, IfcBoolean, IfcLengthMeasure
    instructions="'Anlage' muss definiert sein",
    cardinality="required")


#### Pset_Anex - Allgemeine Anforderungen
spec_01 = ids.Specification(name="Generic specification",
                            description="""HIER STEHT NOCH EINE BESCHREIBUNG""")
spec_01.applicability.extend([ids.Entity(name="IFCVALVE")])

spec_01.requirements.extend([req_dia, req_tag, req_anl])

#### ifcheatexchanger
spec_02 = ids.Specification(name="IfcHeatExchanger specification",
                            description="""HIER STEHT NOCH EINE BESCHREIBUNG""")
spec_02.applicability.append(ids.Entity(name="IFCHEATEXCHANGER"))

spec_02.requirements.extend([req_tag])

#### ifcpipesegment
spec_04 = ids.Specification(name="IfcPipeSegment specification",
                            description="""HIER STEHT NOCH EINE BESCHREIBUNG""")
spec_04.applicability.append(ids.Entity(name="IFCPIPESEGMENT"))

spec_04.requirements.extend([req_len, req_dia])



specs.specifications.append(spec_01)
specs.specifications.append(spec_02)
# Save to a file
os.makedirs("tester", exist_ok=True)
xml_result = specs.to_xml("tester/IDS.xml")
if not xml_result:
    print("Warning: XML validation failed. The IDS file may not be valid.")
os.makedirs("tester", exist_ok=True)
specs.to_xml("tester/IDS.xml")
# Validate IFC model against IDS requirements:
validation_result = specs.validate(my_ifc)
if not validation_result or getattr(validation_result, "failed", False):
    print("Validation failed. Please check the IDS requirements and IFC model.")
else:
    print("Validation succeeded.")

# Show results in a console
# Or to HTML spreadsheet
html_reporter = reporter.Html(specs)
html_reporter.report()
html_reporter.to_file("tester/report.html")
# Or to HTML spreadsheet
report = reporter.Ods(specs)
report.report()
report.to_file("tester/report.ods")


# open tester in browser
webbrowser.open( os.path.abspath("tester/report.html"))