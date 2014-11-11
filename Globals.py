from State_MoveAlongPath import *
from State_Idle import *
from State_Blocked import *

gTileSize = 24
gEntities = []
gStates = {
	"MoveAlongPath": State_MoveAlongPath(),
	"Idle": State_Idle(),
	"Blocked": State_Blocked()
}