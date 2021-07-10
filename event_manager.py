import pygame as pg


class _ReactorEvent:
    """An object for each event"""
    #maybe split the event to: Event and OneTimeEvent that inhrite from Event
    def __init__(self,attribute,key,func,additional):
        self.attribute =attribute
        self.key = key
        self.func = func
        self.additional = additional
        self.one_time= False

class _OneTimeReactorEvent(_ReactorEvent):
    """One time Event - Event that will be destroyed after call"""
    #maybe just use "normal" ReactorEvent if thier is no use to it more than a parameter
    def __init__(self,attribute,key,func,additional):
        super().__init__(attribute,key,func,additional)
        self.one_time = True

class Reactor:
    """Handle all the events in game"""
    def __init__(self,mouse_event_handle_func):
        self._event_fd = {} #Stores the function to active when Event occured {like QUIT , KEYDOWN , MOUSEOUTTON}
        self._events_to_add = []
        self.mouse_event_handle = mouse_event_handle_func


    def add_mouse_event(self,event_type,key, attribute,func,*additional,one_time=False):
        additional = (event_type,func) + additional  # add the type and the func to additional in order to use them in mouse class

        func = self.mouse_event_handle  # change func to mouse handler func
        self.add_event_function(event_type,key, attribute,func,*additional,one_time=one_time)

    def add_event_function(self,event_type,key, attribute,func,*additional,one_time=False):
        """Add event to the event_fd dict. There are events that can happend only one time whick are the one_time and one_time_key"""

        if one_time:
            self._events_to_add.append((event_type,_OneTimeReactorEvent(attribute,key,func,additional)))

        else:
            self._events_to_add.append((event_type,_ReactorEvent(attribute,key,func,additional)))

        self._event_fd.setdefault(event_type,[])


    def activate_functions(self):
        """Loop throght all events and call them if thier signal is on. Runs every frame."""
        for pg_event in pg.event.get():
            for reactor_event in self._event_fd.get(pg_event.type,[]):
                if reactor_event.key == getattr(pg_event,reactor_event.attribute):
                    if reactor_event.additional != ():
                        reactor_event.func(*reactor_event.additional)
                    else:
                        reactor_event.func()

                    if reactor_event.one_time:
                        """There are one time events that need to be removed after Their call"""
                        self._event_fd[pg_event.type].remove(reactor_event)

        self.add_new_events()

    def add_new_events(self): #add new events only after activating the current events becuase i dont want new events to be activate if they were created at the same time the active_evnts function running
        for event_type,event in self._events_to_add:
            self._event_fd[event_type].append(event)

        self._events_to_add = []





  #  def find_event_by_id(self,event_id):
   #     for reactor_events in self._event_fd.values():
    #        for reactor_event in reactor_events:
     #           if reactor_event.id == event_id:
      #              return reactor_event
      #  return None

  #  def change_event(self,event_id,attribute , new_value):
    #    event = self.find_event_by_id(event_id)
       # if event is not None:
       #     setattr(event,attribute,new_value)

    """
        #active key handlers
        for key_code in self._keys_fd:
            if keys[key_code]:
                for handle in self._keys_fd[key_code]:
                    handle()
    """