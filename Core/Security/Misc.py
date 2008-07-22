import os
import types
from DIRAC import S_OK, S_ERROR
from DIRAC.Core.Security.X509Chain import X509Chain
from DIRAC.Core.Security.VOMS import VOMS
from DIRAC.Core.Security import Locations, CS


def getProxyInfo( proxyLoc = False, disableVOMS = False ):
  """
  Returns a dict with all the proxy info
  * values that will be there always
   'path' : path to the file,
   'chain' : chain object containing the proxy
   'subject' : subject of the proxy
   'issuer' : issuer of the proxy
   'isProxy' : bool
   'isLimitedProxy' : bool
   'validDN' : Valid DN in DIRAC
   'validGroup' : Valid Group in DIRAC
   'secondsLeft' : Seconds left
  * values that can be there
   'group' : DIRAC group
   'username' : DIRAC username
   'identity' : DN that generated the proxy
   'hostname' : DIRAC host nickname
   'VOMS'
  """
  if not proxyLoc:
    proxyLoc = Locations.getProxyLocation()

  if not proxyLoc:
    return S_ERROR( "Can't find valid proxy" )

  chain = X509Chain()
  retVal = chain.loadProxyFromFile( proxyLoc )
  if not retVal[ 'OK' ]:
    return S_ERROR( "Can't load %s: %s" % ( proxyLoc, retVal[ 'Message' ] ) )

  retVal = chain.getCredentials()
  if not retVal[ 'OK' ]:
    return retVal

  infoDict = retVal[ 'Value' ]
  infoDict[ 'path' ] = proxyLoc
  infoDict[ 'chain' ] = chain

  if not disableVOMS and chain.isVOMS()['Value']:
    retVal = voms.getVOMSAttributes( proxyLoc )
    if retVal[ 'OK' ]:
      infoDict[ 'VOMS' ] = retVal[ 'Value' ]

  return S_OK( infoDict )

def getProxyInfoAsString( proxyLoc = False, disableVOMS = False ):
  retVal = getProxyInfo( proxyLoc, disableVOMS )
  if not retVal[ 'OK' ]:
    return retVal
  infoDict = retVal[ 'Value' ]
  leftAlign = 13
  contentList = []
  for field in ( 'subject', 'issuer', 'identity', ( 'secondsLeft', 'time left' ),
                 ( 'group', 'DIRAC group' ), 'path', 'username', ( 'VOMS', 'VOMS fqan' ) ):
    if type( field ) == types.StringType:
      dispField = field
    else:
      dispField = field[1]
      field = field[0]
    if not field in infoDict:
      continue
    if field == 'secondsLeft':
      secs = infoDict[ field ]
      hours = int( secs /  3600 )
      secs -= hours * 3600
      mins = int( secs / 60 )
      secs -= mins * 60
      value = "%02d:%02d:%02d" % ( hours, mins, secs )
    else:
      value = infoDict[ field ]
    contentList.append( "%s: %s" % ( dispField.ljust( leftAlign ), value ) )
  return S_OK( "\n".join( contentList ) )
