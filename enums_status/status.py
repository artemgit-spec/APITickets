from enum import Enum

class NewStatusUser(str, Enum): 
    user = 'user'
    admin = 'admin'
    
class StatusTicket(str, Enum):
    all = 'all'
    active = 'active'
    not_active = 'not active'
    
class NewStatus(str, Enum):
    active = 'active'
    not_active = 'not active'