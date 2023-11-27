import json
# Given CSV structure and requirements, let's construct the JSON object for the "BasicInformation" class as requested.

# Defining the basic information based on the provided CSV structure.
basic_information_data = {
    "Bedroom": "A room within a dwelling intended primarily for sleeping",
    "Bathroom": "A room containing a bathtub or shower and typically also a toilet",
    "Property types": "Categories of real estate such as residential, commercial, or industrial",
    "Type of title": "The legal documentation proving ownership of a property, such as freehold or leasehold",
    "Selling method": "The strategy used to sell property, including auction, private treaty, or expression of interest",
    "Floor area": "The total usable surface area within a building, measured in square feet or meters",
    "Land area": "The measure of a plot of land surface",
    "Car Parks": "Designated areas for the parking of vehicles",
    "Open home": "A set time when a property for sale can be viewed by potential buyers",
    "Time on the market": "The duration that a property has been listed for sale",
    "Decade built": "The decade during which a building was constructed",
    "Rating valuation": "An assessment of property value for taxation purposes",
    "Capital growth": "The increase in value of a property over time",
    "Exterior Material": "The materials used for the outside surface of a building",
    "Roof Material": "The materials used to construct the roof of a building",
    "AVM": "Automated Valuation Model, an estimate of a property's market value based on data analysis",
    "CV": "Council Valuation, the value of a property according to local government assessments",
    "IV": "Insurance Valuation, the value of a property for insurance purposes",
    "LV": "Land Valuation, the value of the land component of a property",
    "AgentPrice": "The price a real estate agent estimates a property could sell for",
    "Building concent": "Official permission required to build new structures or alter existing ones",
    "settlement date": "The date on which a property sale is finalized and ownership is transferred",
    "rent apprizeal": "An estimate of how much a property could be rented for",
    "legal description": "A formal description of a property that identifies it for legal purposes",
    "certificate tiitle": "A document that proves ownership of a property",
    "sale history": "The record of past transactions involving a particular property",
    "suburb avm median": "The median Automated Valuation Model value for properties in a suburb",
    "suburb avm median change": "The change in the median AVM value for a suburb over a period of time",
    "rent median price monthly": "The median price of rent for properties in an area per month",
    "rent median price quarter": "The median price of rent for properties in an area per quarter",
    "rent median price year": "The median price of rent for properties in an area per year",
    "estate description": "A detailed description of a property and its features",
    "contour": "Lines on a map which indicate elevation and the shape of the land",
    "Agent": "A person who acts on behalf of another, in particular a real estate agent who arranges the selling, renting, or management of properties"
}

gis_information_data = {
    "bus station": "A designated area where a bus stops for passengers to board or alight",
    "reserve": "Protected area preserved for wildlife, flora, fauna, and historical significance",
    "shopping": "Areas designated for purchasing goods, such as malls or shopping centers",
    "swimming pool": "A constructed basin filled with water for swimming or leisure activities",
    "cinema": "A theatre where movies are shown for public entertainment",
    "hospital": "An institution providing medical and surgical treatment and nursing care for the sick or injured",
    "police station": "A building where police officers work and detain people",
    "gas": "Stations where fuel for vehicles is sold",
    "density": "The number of buildings or inhabitants in a given area",
    "state housing": "Government-provided housing for individuals with low to moderate incomes",
    "neighbourhood ethinicity": "The predominant ethnic groups living in a neighborhood",
    "train station": "A terminal where trains load or unload passengers or goods",
    "ferry station": "A terminal where ferries load or unload passengers or vehicles",
    "flood plain": "An area of land adjacent to a river which is subject to flooding",
    "Unknown": "Information that is not known or has not been disclosed",
    "flood prone": "Areas that are susceptible to flooding",
    "flood sensitive": "Areas that are affected by flooding, often requiring special insurance or building regulations",
    "flow path": "The path that water takes during flooding",
    "zoning": "Legislation for the division of an area into zones in which certain land uses are permitted or prohibited",
    "School zone": "An area around a school with reduced speed limits and special traffic regulations",
    "waste water pipe": "Pipes that carry away sewage or liquid waste",
    "storm water pipe": "Pipes designed to carry rainwater away from urban areas",
    "water pipe": "Pipes that carry drinking water to homes and businesses"
}

image_information_data = {
    "Fence": "A barrier, railing, or other upright structure enclosing an area, typically outdoors, for security or privacy",
    "Trees": "Perennial plants with an elongated stem, or trunk, supporting branches and leaves",
    "Grass": "Vegetation consisting of typically short plants with long narrow leaves, growing wild or cultivated on lawns and pasture",
    "Asbestos": "A heat-resistant fibrous silicate mineral that can be woven into fabrics, and is used in fire-resistant and insulating materials",
    "Style": "The design or make of a particular item, in the context of property, it refers to the architectural design",
    "Slope": "A piece of ground that tends evenly upward or downward",
    "Driveway": "A short private road from the street to a house or garage, used by people who are driving to the house",
    "Ensuite": "A bathroom or toilet that is directly connected to a bedroom",
    "Laundary Room": "A room in a house where clothes are washed and dried",
    "Walkin Wardrobe": "A closet or a small room attached to a bedroom used for clothes storage",
    "Car Port": "A shelter for a car consisting of a roof supported on posts, built beside a house",
    "Exterial Colour": "The color on the outside of a structure",
    "Interial Colour": "The color on the inside of a structure",
    "Chimney": "A vertical channel or pipe which conducts smoke and combustion gases up from a fire or furnace and typically through the roof of a building",
    "Plaster Wall": "A wall coating made from cement, lime, sand, or gypsum, used to coat walls and ceilings",
    "Garage": "A building or indoor area for parking or storing motor vehicles"
}

invisible_information_data = {
    "home loan": "A sum of money borrowed from a financial institution to purchase a house",
    "good for kids": "An attribute of a property indicating that it has features suitable for children",
    "Family": "Refers to a living space that is designed to accommodate a group of people related by blood or law",
    "Elderly": "Suitability of a property for older individuals, possibly with accessibility features",
    "Privacy": "The state of being free from public attention within a property, often through strategic design or location",
    "safety": "The condition of being protected from or unlikely to cause danger, risk, or injury within a property",
    "Pet": "The allowance or suitability of a property for animals kept for companionship",
    "Storage": "The space or features within a property designed to store goods and items",
    "Ensuite": "A private bathroom attached to a bedroom",
    "subsection": "A division of a larger area, typically for administrative purposes within property development",
    "Garage": "A walled, roofed structure for storing a vehicle or vehicles, typically attached to or part of a house",
    "seaview": "A feature of a property that includes a view of the sea",
    "mountainview": "A feature of a property that includes a view of mountains",
    "cityview": "A feature of a property that includes a view of a cityscape"
}


# Define a function to convert data dictionaries into the required JSON format
def convert_to_json_format(**data_categories):
    class_json = {"Class": {}}

    for category, data in data_categories.items():
        class_json["Class"][category] = [{"key": key, "description": description} for key, description in data.items()]

    return class_json


# Assuming the existence of four dictionaries with the same structure as the ones we created above:
# basic_information_data, gis_information_data, image_information_data, invisible_information_data
# You would call the function like this:
combined_json = convert_to_json_format(
    basic_information_data=basic_information_data,
    gis_information_data=gis_information_data,
    image_information_data=image_information_data,
    invisible_information_data=invisible_information_data
)

# Now let's save this combined JSON object to a file.
json_file_path = 'issue.json'
with open(json_file_path, 'w') as json_file:
    json.dump(combined_json, json_file, indent=4)