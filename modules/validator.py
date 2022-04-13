import re

def CheckEmail(email: str) -> bool: 
    assert type(email) != "<class 'int'>", "Email isn't string"
    validacion = re.compile(r"""
    \b [\w.%+-] +@ [a-zA-Z.-] +\. [a-zA-Z]{2,6} \b """, re.X
    )
    email = validacion.findall(email)

    if len(email) == 0:
        return False
    return True

def CheckPhoneNumber(phoneNumber):
    
    validacion = re.compile(r"""
    ^ [0-9]{10} $""", re.X
    )

    if str(type(phoneNumber))=="<class 'int'>": 
        phoneNumber=str(phoneNumber) 
        phoneNumber = validacion.findall(phoneNumber)
    
    if len(phoneNumber) == 0:
        return False
    return True

def CheckDocument(cedula):
    
    validacion = re.compile(r"""
    ^ [0-9]{10} $""", re.X
    )

    if str(type(cedula))=="<class 'int'>": phoneNumber=str(cedula) 
    cedula = validacion.findall(cedula)
        
    if len(cedula) == 0:
        return False
    return True
