# This file mainly focusing on construction structral data in order to contrute GNN for a demo test.

# all the issues are here:
# issue = ['Bus Stop', 'Ferry Station', 'Hospital', 'Police Station', 'School Zone', 'Train Station', 'City View', 'Fence',
#          'Grass', 'Mountain View', 'Sea View', 'Trees', 'Agent', 'Capital Growth', 'Contour', 'Decade Built', 'Floor Area',
#          'Land Area', 'Open Home', 'Property Types', 'Rating Valuation', 'Rent Appraisal', 'Sale History', 'Selling Method',
#          'Settlement Date', 'Subsection', 'Time On The Market', 'Type Of Title', 'Bar', 'Cafe', 'Cinema', 'Gas', 'Gym',
#          'Pharmacy', 'Reserve', 'Restaurant', 'Shopping', 'Swimming Pool', 'Flood Plain', 'Flood Prone', 'Flood Sensitive',
#          'Flow Path', 'Waste Water Manhole', 'Storm Water Manhole', 'Zoning', 'Asbestos', 'Car Port', 'Chimney', 'Driveway',
#          'Exterior Color', 'Exterior Colour', 'Exterior Material', 'Garage', 'Plaster Wall', 'Roof Material', 'Slope',
#          'Storage', 'Storm Water Pipe', 'Waste Water Pipe', 'Water Pipe', 'Home Loan', 'Bathroom', 'Bedroom', 'Ensuite',
#          'Interior Color', 'Interior Colour', 'Laundry Room', 'Open Kitchen', 'Granny Room', 'Stairs', 'Style',
#          'Walkin Wardrobe', 'Age distribution', 'Average Time In The Home', 'Dense Housing', 'Income Distribution',
#          'Neighbourhood Ethnicity', 'Occupancy', 'Occupation Distribution', 'Ownership Distribution', 'Population Density',
#          'Building Consent', 'Certificate Title', 'Legal Description', 'State Housing', 'AVM', 'AgentPrice', 'Council Valuation',
#          'Insurance Valuation', 'Land Valuation', 'Real Estate Description', 'Rent Median Price Monthly', 'Rent Median Price Quarter',
#          'Rent Median Price Year', 'Suburb AVM Median', 'Suburb AVM Median Change', 'Elderly', 'Family', 'Good For Kids',
#          'Pet', 'Privacy', 'Safety']



# The expected data structure is following
# data = {
#     {
#         "UserID": "string",
#         "Property": {
#             {
#                 "PropertyID": "string",
#                 "Issue": list
#             },
#             {
#                 "PropertyID": "string",
#                 "Issue": list
#             }
#         },
#         "Conversation": list
#     },
#     {
#         "UserID": "string",
#         "Property": {
#             {
#                 "PropertyID": "string",
#                 "Issue": list
#             },
#             {
#                 "PropertyID": "string",
#                 "Issue": list
#             }
#         },
#         "Conversation": list
#     }
# }

issue = ['Bus Stop', 'Ferry Station', 'Hospital', 'Police Station', 'School Zone', 'Train Station', 'City View', 'Fence',
         'Grass', 'Mountain View', 'Sea View', 'Trees', 'Agent', 'Capital Growth', 'Contour', 'Decade Built', 'Floor Area',
         'Land Area', 'Open Home', 'Property Types', 'Rating Valuation', 'Rent Appraisal', 'Sale History', 'Selling Method',
         'Settlement Date', 'Subsection', 'Time On The Market', 'Type Of Title', 'Bar', 'Cafe', 'Cinema', 'Gas', 'Gym',
         'Pharmacy', 'Reserve', 'Restaurant', 'Shopping', 'Swimming Pool', 'Flood Plain', 'Flood Prone', 'Flood Sensitive',
         'Flow Path', 'Waste Water Manhole', 'Storm Water Manhole', 'Zoning', 'Asbestos', 'Car Port', 'Chimney', 'Driveway',
         'Exterior Color', 'Exterior Colour', 'Exterior Material', 'Garage', 'Plaster Wall', 'Roof Material', 'Slope',
         'Storage', 'Storm Water Pipe', 'Waste Water Pipe', 'Water Pipe', 'Home Loan', 'Bathroom', 'Bedroom', 'Ensuite',
         'Interior Color', 'Interior Colour', 'Laundry Room', 'Open Kitchen', 'Granny Room', 'Stairs', 'Style',
         'Walkin Wardrobe', 'Age distribution', 'Average Time In The Home', 'Dense Housing', 'Income Distribution',
         'Neighbourhood Ethnicity', 'Occupancy', 'Occupation Distribution', 'Ownership Distribution', 'Population Density',
         'Building Consent', 'Certificate Title', 'Legal Description', 'State Housing', 'AVM', 'AgentPrice', 'Council Valuation',
         'Insurance Valuation', 'Land Valuation', 'Real Estate Description', 'Rent Median Price Monthly', 'Rent Median Price Quarter',
         'Rent Median Price Year', 'Suburb AVM Median', 'Suburb AVM Median Change', 'Elderly', 'Family', 'Good For Kids', 'Pet', 'Privacy', 'Safety']