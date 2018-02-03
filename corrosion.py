""" This module contains corrosion experiments."""


#######################################################
class metal_plate:

    # This is a virtual metal plate for comparitive corrosion experiments.
    # It is 1.0 square meter in area and 1 mm (1000 micrometers) thick.

    def __init__(self):

        self.thickness = [1000]                 # micrometers
        self.soluble_products = [0]             # micrometers
        self.insoluble_products = [0]           # micrometers
        self.effluent_volume = [0]              # liters
        self.effluent_concentration = [0]       # grams/liter
        self.corrosion_rate_k = None            # 1/(RH*Hr)
        self.rain_reaction_rate_k = None        #
        self.runoff_rate_k = 1                  # 1/(mm*Hr)
        self.time_domain =[]                    # datetime


    def corrode(self,RH):

        # This function simulates electrolytic corrosion
        # of the zinc surface when exposed to humid air.

        if RH > 70:

            # calculate corrosion products using mass action
            corrosion_products = (self.corrosion_rate_k * (RH/100.0))

            # calculate thickness at next time step
            self.thickness.append(self.thickness[-1] - corrosion_products)

            # apportion corrosion products, 80% soluble vs. 20% insoluble
            self.soluble_products.append(self.soluble_products[-1] + (0.8*corrosion_products))
            self.insoluble_products.append(self.insoluble_products[-1] + (0.2*corrosion_products))

        else:

            # increment lists for dimensionality
            self.thickness.append(self.thickness[-1])
            self.soluble_products.append(self.soluble_products[-1])
            self.insoluble_products.append(self.insoluble_products[-1])


    def runoff(self,precip):

        # This function estimates the loss of soluble corrosion products
        # during a precipitation event.

        if precip > 0:

            # calculate corrosion products using zeroith order action
            runoff_products = (self.rain_reaction_rate_k)

            # remove runoff products from metal thickness
            self.thickness[-1] -= runoff_products

            # calculate effluent volume in m^3 (precipitation in meters times the area, 1 m^2)
            self.effluent_volume.append(precip*0.0254)

            # Calculate loss with mass action rate linearly scaled with precipitation
            soluble_loss = (self.soluble_products[-1] * self.runoff_rate_k * precip)

            # calculate soluble products at current time step.
            self.soluble_products[-1] -= soluble_loss

            # calculate effluent concentration
            self.effluent_concentration.append(((soluble_loss + runoff_products)*7.14)/self.effluent_volume[-1])

        else:

            # increment lists for dimensionality
            self.effluent_concentration.append(0)
            self.effluent_volume.append(0)
#######################################################
#######################################################
class zinc_plate(metal_plate):

# This metal_plate has properties consistent with zinc.

    def __init__(self):
        metal_plate.__init__(self)
        self.corrosion_rate_k = 0.0002          # 1/(RH*Hr)
        self.rain_reaction_rate_k = 0.00000005  #
        self.runoff_rate_k = 1                  # 1/(mm*Hr)


#######################################################
class weather:

    # This class stores meteorological data for easy plotting.
    # It's just a convenient way to grab some values from the
    # SQL query during the simulation.

    def __init__(self):

        self.time_domain =[]    # datetime
        self.temp = []          # Temperature
        self.RH = []            # Relative Humidity
        self.precip = []        # Precipitation

    def get_conditions(self,dt_obj,T,Rhum,rain):

        self.time_domain.append(dt_obj)    # datetime
        self.temp.append(T)                # Temperature
        self.RH.append(Rhum)               # Relative Humidity
        self.precip.append(rain*25.4)      # Precipitation convert to mm

#######################################################
