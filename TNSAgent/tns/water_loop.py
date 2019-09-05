########################################
## Cold water thermal loop as a neighbor node
from datetime import timedelta, datetime

from neighbor import Neighbor
from neighbor_model import NeighborModel
from local_asset import LocalAsset
from myTransactiveNode import myTransactiveNode
from meter_point import MeterPoint
from measurement_type import MeasurementType
from measurement_unit import MeasurementUnit
from temperature_forecast_model import TemperatureForecastModel
from market import Market
from market_state import MarketState
from auction import Auction
from vertex import Vertex
from helpers import prod_cost_from_vertices
from interval_value import IntervalValue

# create a neighbor model 
water_loop = myTransactiveNode()
mTN = water_loop
mTN.description = 'cold water ddistribution loop on campus'
mTN.name = 'water_loop'

# set up meter point
cold_meter = MeterPoint()
MP = cold_meter
MP.description = 'meters mass flowrate through cold water loop'
MP.measurementType = MeasurementType.Cooling
MP.measurement = MeasurementUnit.kWh
cold_meter = MP

# provide a cell array of all Meterpoints to myTransactiveNode
mTN.meterpoints = [cold_meter]

# instantiate each information service model
# this is services that can be queried for information
# this includes model prediction for future time intervals
# Pullman Temperature Forecast <-- Information service model
PullmanTemperatureForecast = TemperatureForecastModel()
ISM = PullmanTemperatureForecast
ISM.name = 'PullmanTemperatureForecast'
ISM.predictedValues = [] # dynamically assigned

mTN.informationServiceModels = [PullmanTemperatureForecast]

#######################################################################
## Intantiate Markets
# Markets specify active TimeIntervals

## Day Ahead Market
dayAhead = Market(measurementType = [MeasurementType.Cooling])
MKT = dayAhead
MKT.name = 'waterloop_Market'
MKT.commitment = False # start without having commited any resources
MKT.converged = False # start without having converged
MKT.defaultPrice = [0.03] # [$/kWh]
MKT.dualityGapThreshold = 0.001 #optimal convergence within 0.1Wh
MKT.futureHorizon = timedelta(hours=24)
MKT.intervalDuration = timedelta(hours=1)
MKT.intervalsToClear = 24
MKT.marketClearingTime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) # align with top of hour
MKT.marketOrder = 1 # this is the first and only market
MKT.nextMarketClearingTime = MKT.marketClearingTime + timedelta(hours=1)
MKT.initialMarketState = MarketState.Inactive
dayAhead = MKT
dayAhead.check_intervals()

ti = dayAhead.timeIntervals
# Thermal Loops are seen as neighbor nodes

mTN.markets = [dayAhead]

######################################################################################################################

## instantiate neighbors and neighbor models
# this node only has the utility and thermal loops as neighbors
TUR111 = Neighbor()
NB = TUR111
NB.lossFactor = 0.01
NB.mechanism = 'consensus'
NB.description = 'substation TUR111 includes SCUE building and and connection with AVISTA'
NB.maximumPower = -10000
NB.minimumPower = 0
NB.name = 'T111'

TUR111Model = NeighborModel(measurementType=[MeasurementType.PowerReal, MeasurementType.Heat, MeasurementType.Cooling])
NBM = TUR111Model
NBM.name = 'TUR111Model'
NBM.converged = False
NBM.convergenceThreshold = 0.02
NBM.effectiveImpedance = 0.0
NBM.friend = True
NBM.transactive = True
NB.model = NBM
NBM.object = NB
TUR111 = NB
TUR111Model = NBM

# TUR115
TUR115 = Neighbor()
NB = TUR115
NB.lossFactor = 0.01
NB.mechanism = 'consensus'
NB.description = 'substation TUR115 includes SCUE building and and connection with AVISTA'
NB.maximumPower = -10000
NB.minimumPower = 0
NB.name = 'T115'

TUR115Model = NeighborModel(measurementType=[MeasurementType.PowerReal, MeasurementType.Heat, MeasurementType.Cooling])
NBM = TUR115Model
NBM.name = 'TUR115Model'
NBM.converged = False
NBM.convergenceThreshold = 0.02
NBM.effectiveImpedance = 0.0
NBM.friend = True
NBM.transactive = True
NB.model = NBM
NBM.object = NB
TUR115 = NB
TUR115Model = NBM

# TVW131
TVW131 = Neighbor()
NB = TVW131
NB.lossFactor = 0.01
NB.mechanism = 'consensus'
NB.description = 'substation TVW131 feeds the east campus chillers,\
    clark hall and its chillers, and some inflexible east campus loads.'
NB.maximumPower = -10000
NB.minimumPower = 0
NB.name = 'T131'

TVW131Model = NeighborModel(measurementType=[MeasurementType.PowerReal, MeasurementType.Heat, MeasurementType.Cooling])
NBM = TVW131Model
NBM.name = 'TVW131Model'
NBM.converged = False
NBM.convergenceThreshold = 0.02
NBM.effectiveImpedance = 0.0
NBM.friend = True
NBM.transactive = True
NB.model = NBM
NBM.object = NB
TVW131 = NB
TVW131Model = NBM

#SPU122
SPU122 = Neighbor()
NB = SPU122
NB.lossFactor = 0.01
NB.mechanism = 'consensus'
NB.description = 'substation SPU122 feeds half of the grimes way steam plant\
    as well as the central campus inflexible buildings'
NB.maximumPower = -10000
NB.minimumPower = 0
NB.name = 'S122'

SPU122Model = NeighborModel(measurementType=[MeasurementType.PowerReal, MeasurementType.Heat, MeasurementType.Cooling])
NBM = SPU122Model
NBM.name = 'SPU122Model'
NBM.converged = False
NBM.convergenceThreshold = 0.02
NBM.effectiveImpedance = 0.0
NBM.friend = True
NBM.transactive = True
NB.model = NBM
NBM.object = NB
SPU122 = NB
SPU122Model = NBM

# SPU124
SPU124 = Neighbor()
NB = SPU124
NB.lossFactor = 0.01
NB.mechanism = 'consensus'
NB.description = 'substation SPU124 feeds half of the grimes way steam plant\
    as well as Johnson hall and the east campus inflexible buildings'
NB.maximumPower = -10000
NB.minimumPower = 0
NB.name = 'S124'

SPU124Model = NeighborModel(measurementType=[MeasurementType.PowerReal, MeasurementType.Heat, MeasurementType.Cooling])
NBM = SPU124Model
NBM.name = 'SPU124Model'
NBM.converged = False
NBM.convergenceThreshold = 0.02
NBM.effectiveImpedance = 0.0
NBM.friend = True
NBM.transactive = True
NB.model = NBM
NBM.object = NB
SPU124 = NB
SPU124Model = NBM

#SPU 125
SPU125 = Neighbor()
NB = SPU125
NB.lossFactor = 0.01
NB.mechanism = 'consensus'
NB.description = 'substation SPU125 feeds half of the College Ave Steam plant. \
                    including the West campus chillers, half of the west campus \
                    inflexible buildings, and the CASP boilers.'
NB.maximumPower = -10000
NB.minimumPower = 0
NB.name = 'S125'

SPU125Model = NeighborModel(measurementType=[MeasurementType.PowerReal, MeasurementType.Heat, MeasurementType.Cooling])
NBM = SPU125Model
NBM.name = 'SPU125Model'
NBM.converged = False
NBM.convergenceThreshold = 0.02
NBM.effectiveImpedance = 0.0
NBM.friend = True
NBM.transactive = True
NB.model = NBM
NBM.object = NB
SPU125 = NB
SPU125Model = NBM

# create list of transactive neighbors to the cold water loop
mTN.neighbors = [TUR111, TUR115, TVW131, SPU122, SPU124, SPU125]

###########################################################################################
# instantiate each Local Asset and its LocalAssetModel
# a LocalAsset is "owned" by myTransactiveNode and is managed and 
# represented by a LocalAssetModel. There must be a one to one
# correspondence between a model and its asset

# Cooling loop does not own it's own local assets.
# possibly need to put cold thermal storage here

#############################################################################
## Additional setup script
# the following methods would normally be called soon after the above script
# to launch the system
# 
# call the Market method that will instantiate active future time intervals
dayAhead.check_intervals()

# call the information service that predicts and stores outdoor temps
PullmanTemperatureForecast.update_information(dayAhead)

# recieve any transactive signals sent to myTransactiveNode from its
# TransactiveNeighbors.
TUR111Model.receive_transactive_signal(water_loop)
TUR115Model.receive_transactive_signal(water_loop)
TVW131Model.receive_transactive_signal(water_loop)
SPU122Model.receive_transactive_signal(water_loop)
SPU124Model.receive_transactive_signal(water_loop)
SPU125Model.receive_transactive_signal(water_loop)

#balance supply and demand at myTransactiveNode. This is iterative. A
# succession of iterationcounters and duality gap (the convergence metric)
# will be generated until the system converges. All scheduled powers and
# marginal prices should be meaningful for all active time intervals at the
# conclusion of this method
dayAhead.balance(water_loop)

# myTransactiveNode must prepare a set of TransactiveRecords for each of 
# its TransactiveNeighbors. The records are updated and stored into the
# property "mySignal" of the TransactiveNeighbor.
TUR111Model.prep_transactive_signal(dayAhead, water_loop)
TUR115Model.prep_transactive_signal(dayAhead, water_loop)
TVW131Model.prep_transactive_signal(dayAhead, water_loop)
SPU122Model.prep_transactive_signal(dayAhead, water_loop)
SPU124Model.prep_transactive_signal(dayAhead, water_loop)
SPU125Model.prep_transactive_signal(dayAhead, water_loop)

# Finally, the prepared TransactiveRecords are sent to their corresponding
# TransactiveNeighbor.
TUR111Model.send_transactive_signal(water_loop)
TUR115Model.send_transactive_signal(water_loop)
TVW131Model.send_transactive_signal(water_loop)
SPU122Model.send_transactive_signal(water_loop)
SPU124Model.send_transactive_signal(water_loop)
SPU125Model.send_transactive_signal(water_loop)

# invoke the market object to sum all powers as will be needed by the 
# net supply/demand curve
dayAhead.assign_system_vertices(water_loop)

# view the system supply/demand curve
dayAhead.view_net_curve(0, MeasurementType.Cooling)