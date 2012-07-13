# $HeadURL:  $
''' PEP

  Module used for enforcing policies. Its class is used for:
    1. invoke a PDP and collects results
    2. enforcing results by:
       a. saving result on a DB
       b. raising alarms
       c. other....
'''

#from DIRAC                                                       import S_ERROR
from DIRAC.ResourceStatusSystem.Client.ResourceStatusClient      import ResourceStatusClient
from DIRAC.ResourceStatusSystem.Client.ResourceManagementClient  import ResourceManagementClient
#from DIRAC.ResourceStatusSystem.PolicySystem.Actions.EmptyAction import EmptyAction
from DIRAC.ResourceStatusSystem.PolicySystem.PDP                 import PDP
#from DIRAC.ResourceStatusSystem.Utilities                        import Utils

__RCSID__  = '$Id:  $'

class PEP:
#  '''
#  PEP (Policy Enforcement Point) initialization
#
#  :params:
#    :attr:`granularity`       : string - a ValidElement (optional)
#    :attr:`name`              : string - optional name (e.g. of a site)
#    :attr:`status`            : string - optional status
#    :attr:`formerStatus`      : string - optional former status
#    :attr:`reason`            : string - optional reason for last status change
#    :attr:`siteType`          : string - optional site type
#    :attr:`serviceType`       : string - optional service type
#    :attr:`resourceType`      : string - optional resource type
#    :attr:`futureEnforcement` :          optional
#      [
#        {
#          'PolicyType': a PolicyType
#          'Granularity': a ValidElement (optional)
#        }
#      ]
#  '''

  def __init__( self, clients = None ):
#    '''
#    Enforce policies, using a PDP  (Policy Decision Point), based on
#
#     self.__granularity (optional)
#     self.__name (optional)
#     self.__status (optional)
#     self.__formerStatus (optional)
#     self.__reason (optional)
#     self.__siteType (optional)
#     self.__serviceType (optional)
#     self.__realBan (optional)
#     self.__user (optional)
#     self.__futurePolicyType (optional)
#     self.__futureGranularity (optional)
#
#     :params:
#       :attr:`clients`   : a dictionary containing modules corresponding to clients.
#    '''
   
    if clients is None:
      clients = {}
   
    if 'ResourceStatusClient' in clients:           
      self.rsClient = clients[ 'ResourceStatusClient' ]
    else:
      self.rsClient = ResourceStatusClient()
    if 'ResourceManagementClient' in clients:             
      self.rmClient = clients[ 'ResourceManagementClient' ]
    else: 
      self.rmClient = ResourceManagementClient()

    self.pdp = PDP( clients )

#  def enforce( self, element = None, name = None, statusType = None, 
#               status = None, formerStatus = None, reason = None, 
#               elementType = None, tokenOwner = None ):

  def enforce( self, decissionParams ):
    
    '''
      Enforce policies for given set of keyworkds. To be better explained.
    '''
  
    ##  real ban flag  #########################################################

#    realBan = False
#    if tokenOwner is not None:
#      if tokenOwner == 'rs_svc':
#        realBan = True
   
    ## policy setup ############################################################  

#    decissionParams = {}
#    localParams     = locals()
#    
#    # Small workaround to avoid deleting from locals() 
#    for lParamK, lParamV in localParams.items():
#      if lParamK != 'self':
#        decissionParams[ lParamK ] = lParamV
    
    self.pdp.setup( decissionParams )

    ## policy decision #########################################################

    resDecisions = self.pdp.takeDecision()

# commented out for a while, while development is ongoing.

#    ## record all results before doing anything else    
#    for resP in resDecisions[ 'SinglePolicyResults' ]:
#      
#      if not resP.has_key( 'OLD' ):       
#        self.clients[ "rmClient" ].insertPolicyResultLog( granularity, name,
#                                                          resP[ 'PolicyName' ], 
#                                                          statusType,
#                                                          resP[ 'Status' ], 
#                                                          resP[ 'Reason' ], now )
#        
#      else:
#        gLogger.warn( 'OLD: %s' % resP )
#        
#    res          = resDecisions[ 'PolicyCombinedResult' ] 
#    actionBaseMod = "DIRAC.ResourceStatusSystem.PolicySystem.Actions"
#
#    # Security mechanism in case there is no PolicyType returned
#    if res == {}:
#      EmptyAction(granularity, name, statusType, resDecisions).run()
#
#    else:
#      policyType   = res[ 'PolicyType' ]
#
#      if 'Resource_PolType' in policyType:
#        action = Utils.voimport( '%s.ResourceAction' % actionBaseMod )
#        action.ResourceAction(granularity, name, statusType, resDecisions,
#                         rsClient=self.rsClient,
#                         rmClient=self.rmClient).run()
#
#      if 'Alarm_PolType' in policyType:
#        action = Utils.voimport( '%s.AlarmAction' % actionBaseMod )
#        action.AlarmAction(granularity, name, statusType, resDecisions,
#                       Clients=self.clients,
#                       Params={"Granularity"  : granularity,
#                               "SiteType"     : siteType,
#                               "ServiceType"  : serviceType,
#                               "ResourceType" : resourceType}).run()
#
#      if 'RealBan_PolType' in policyType and realBan:
#        action = Utils.voimport( '%s.RealBanAction' % actionBaseMod )
#        action.RealBanAction(granularity, name, resDecisions).run()

    return resDecisions

################################################################################
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF