
try:
    from java.awt import Robot, Toolkit
    from java.awt.event import InputEvent
    from java.awt.MouseInfo import getPointerInfo
    import time

    r = Robot()
    move_mouse_right = True
    while True:
        loc = getPointerInfo().getLocation()
        x = int(loc.getX())
        y = int(loc.getY())
        print(x,y)
        if move_mouse_right:
            r.mouseMove(x+1,y)
        else:
            r.mouseMove(x-1,y)
        if move_mouse_right:
            move_mouse_right = False
        else:
            move_mouse_right = True
        time.sleep(10)

except Exception as e:
    print(e)
