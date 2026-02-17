from kepoco import display, buttonA, buttonB

def wait_for_button_release():
    # Waits until the user is no longer pressing either button.
    while buttonA.pressed() or buttonB.pressed():
        pass

# Screen
screen_width = 72
screen_height = 40
ground_height = 5

# Rocket
rocket_width = 7
rocket_height = 5
gravity = 0.02
boost_strength = -0.7

# Asteroid Barrier
asteroid_width = 10
asteroid_gap = 15

# Digits for Score Display
digits_display = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def new_game():
    return {
        "rocket_x": 20,
        "rocket_y": 20,
        "rocket_velocity": 0,
        "Asteroid_barrier_x": 100, # X position of the asteroid barrier
        "Asteroid_barrier_y": 15, # Y position of the asteroid barrier
        "running": True, # Is the game active?
        "started": False, # Has the countdown finished?
        "score": 0,
        "scored_this_pipe": False, # Prevents scoring twice on one barrier
        "pipe_variation_state": 0,
        "pipe_speed": 1,
        "speed_level": 0
    }

def update_rocket(game):
    
    # It Updates the rocket's position based on gravity and velocity.
    if not game["started"]:
        return
    game["rocket_velocity"] += gravity
    game["rocket_y"] += game["rocket_velocity"]
    ground_line_y = screen_height - ground_height
    
    # Check for top or ground collision
    if game["rocket_y"] < 0 or game["rocket_y"] + rocket_height > ground_line_y:
        game["running"] = False

def update_pipes(game):
    
    # Moves the asteroid barriers and handles scoring and resetting
    if not game["started"]:
        return
    game["Asteroid_barrier_x"] -= 1

    # Check for scoring
    if game["Asteroid_barrier_x"] + asteroid_width < game["rocket_x"] and not game["scored_this_pipe"]:
        game["score"] += 1
        game["scored_this_pipe"] = True

    # Check for barrier reset
    if game["Asteroid_barrier_x"] < -asteroid_width:
        game["Asteroid_barrier_x"] = screen_width
        game["scored_this_pipe"] = False
        
        # Cycle through 3 gap heights for variation
        game["pipe_variation_state"] += 1
        if game["pipe_variation_state"] > 2:
            game["pipe_variation_state"] = 0
            
        # Set gap height based on the state
        if game["pipe_variation_state"] == 0:
            game["Asteroid_barrier_y"] = 15 # Medium Height
        elif game["pipe_variation_state"] == 1:
            game["Asteroid_barrier_y"] = 25 # Low Height
        else: # state == 2
            game["Asteroid_barrier_y"] = 5  # High Height

    check_pipe_collision(game)

def check_pipe_collision(game):
    
    # Checks for intersection between the rocket and the asteroid barriers
    rx = game["rocket_x"]
    ry = game["rocket_y"]
    px = game["Asteroid_barrier_x"]
    gy = game["Asteroid_barrier_y"]
    gap = asteroid_gap
    if rx + rocket_width > px and rx < px + asteroid_width:
        # Check collision with top barrier (rocket is above the gap)
        if ry < gy:
            game["running"] = False
        # Check collision with bottom barrier (rocket is below the gap)
        if (ry + rocket_height) > (gy + gap):
            game["running"] = False

# Rocket Sprite

def draw_rocket_straight(game):
    rx = int(game["rocket_x"])
    ry = int(game["rocket_y"])
    
    # Main Body (5x3 block)
    display.drawFilledRectangle(rx + 1, ry + 1, 5, 3, display.WHITE)

    #Nose Cone (1x1 point)
    display.drawFilledRectangle(rx + 6, ry + 2, 1, 1, display.WHITE)

    #Wings (1x1 on the side)
    display.drawFilledRectangle(rx, ry + 1, 1, 1, display.WHITE)
    display.drawFilledRectangle(rx, ry + 3, 1, 1, display.WHITE)
    
    #Flame (1x1 Black)
    display.drawFilledRectangle(rx - 1, ry + 2, 1, 1, display.BLACK)

def draw_rocket_up(game):
    rx = int(game["rocket_x"])
    ry = int(game["rocket_y"])
    
    # Main Body (5x3 block)
    display.drawFilledRectangle(rx + 1, ry + 0, 5, 3, display.WHITE)

    # Cone (1x1 point)
    display.drawFilledRectangle(rx + 6, ry + 1, 1, 1, display.WHITE)

    # Wings (1x1 on the side)
    display.drawFilledRectangle(rx, ry + 0, 1, 1, display.WHITE)
    display.drawFilledRectangle(rx, ry + 2, 1, 1, display.WHITE)
    
    # Flame (1x1 Black)
    display.drawFilledRectangle(rx - 1, ry + 1, 1, 1, display.BLACK)

def draw_rocket_down(game):
    rx = int(game["rocket_x"])
    ry = int(game["rocket_y"])
    
    # Main Body (5x3 block)
    display.drawFilledRectangle(rx + 1, ry + 2, 5, 3, display.WHITE)

    # Cone (1x1 point)
    display.drawFilledRectangle(rx + 6, ry + 3, 1, 1, display.WHITE)

    # Wings (1x1 on the side)
    display.drawFilledRectangle(rx, ry + 2, 1, 1, display.WHITE)
    display.drawFilledRectangle(rx, ry + 4, 1, 1, display.WHITE)

    # Flame (1x1 Black)
    display.drawFilledRectangle(rx - 1, ry + 3, 1, 1, display.BLACK)

def draw_rocket(game):

    velocity = game["rocket_velocity"]
    if velocity < -0.1: # Boosting
        draw_rocket_up(game)
    elif velocity > 0.1: # Falling
        draw_rocket_down(game)
    else: #
        draw_rocket_straight(game)

def draw_asteroids(game):
    px = game["Asteroid_barrier_x"]
    gy = game["Asteroid_barrier_y"]
    aw = asteroid_width

    # Top Asteroid/Barrier (Main white block)
    display.drawFilledRectangle(px, 0, aw, gy, display.WHITE)
    
    # Add debris inside the top block (Black dots)
    if gy > 5:
        # Rocks near the top
        display.drawFilledRectangle(px + 2, 3, 1, 1, display.BLACK) 
        # Rocks near the gap
        display.drawFilledRectangle(px + 7, gy - 3, 1, 1, display.BLACK) 
    
    # Bottom Asteroid/Barrier (Main white block)
    bottom_y = gy + asteroid_gap
    height = screen_height - bottom_y
    display.drawFilledRectangle(px, bottom_y, aw, height, display.WHITE)

    # Add debris inside the bottom block (Black dots)
    if height > 5:
        # Rocks near the top of the bottom block
        display.drawFilledRectangle(px + 3, bottom_y + 2, 1, 1, display.BLACK)
        # Rocks near the bottom
        display.drawFilledRectangle(px + 8, bottom_y + height - 3, 1, 1, display.BLACK)

def draw_start_screen():
    display.fill(display.BLACK)
    display.drawText("Rocket Dash", 1, 1, display.WHITE)
    display.drawText("A to Start", 1, 20, display.WHITE)
    display.drawText("B to Quit", 1, 32, display.WHITE)
    display.update()

def draw_score(game):
    score = game["score"]
    tens_value = score // 10 
    if tens_value >= 10:
        tens_value = tens_value % 10
    ones_value = score % 10

    # Draw tens digit
    tens_char = digits_display[int(tens_value)]
    display.drawText(tens_char, screen_width - 15, 1, display.WHITE)

    # Draw ones digit
    ones_char = digits_display[int(ones_value)]
    display.drawText(ones_char, screen_width - 10, 1, display.WHITE)

def draw_pause():
    # Draws the instruction for pausing the gam,
    hint_x = screen_width - 72
    display.drawText("B to", hint_x, 1, display.WHITE)
    display.drawText("Pause", hint_x, 10, display.WHITE)

def draw_ground():
    ground_y = screen_height - ground_height
    
    # Draw the main white ground bar
    display.drawFilledRectangle(0, ground_y, screen_width, ground_height, display.WHITE )

    # Black debris inside the white ground bar
    display.drawFilledRectangle(2, screen_height - 2, 1, 1, display.BLACK)
    display.drawFilledRectangle(10, screen_height - 1, 1, 1, display.BLACK)
    display.drawFilledRectangle(25, screen_height - 3, 1, 1, display.BLACK)
    display.drawFilledRectangle(38, screen_height - 2, 2, 1, display.BLACK)
    display.drawFilledRectangle(55, screen_height - 4, 1, 1, display.BLACK)
    display.drawFilledRectangle(70, screen_height - 1, 1, 1, display.BLACK)

def draw_game(game):
    display.fill(display.BLACK)
    draw_rocket(game)
    draw_asteroids(game)
    draw_ground()
    draw_score(game)
    if game["started"] and game["running"]:
        draw_pause()
    display.update()

def game_over_screen(score): 
    display.fill(display.BLACK)
    display.drawText("GAME OVER", 5, 1, display.WHITE)
    
    # Calculate score digits for display
    tens_value = score // 10
    if tens_value >= 10:
        tens_value = tens_value % 10 
    ones_value = score % 10
    score_text_x = 1
    display.drawText("Score:", score_text_x, 12, display.WHITE) 
    tens_x = 40
    tens_char = digits_display[int(tens_value)]
    display.drawText(tens_char, tens_x, 12, display.WHITE)
    ones_x = tens_x + 5 
    ones_char = digits_display[int(ones_value)]
    display.drawText(ones_char, ones_x, 12, display.WHITE)
    display.drawText("A to Restart", 1, 22, display.WHITE)
    display.drawText("B to Quit", 1, 32, display.WHITE)
    display.update() 
    while True:
        if buttonA.justPressed():
            return "restart"
        if buttonB.justPressed():
            return "quit"

def pause_screen(game):
    display.fill(display.BLACK)
    display.drawText("PAUSED", 15, 1, display.WHITE)
    display.drawText("B to Resume", 1, 25, display.WHITE)
    display.update()
    
    # Wait for B press to unpause
    while True:
        if buttonB.justPressed():
            break 
            
    # Resume Countdown Loop (3, 2, 1, GO!)
    wait_for_button_release() # Clear any button presses before countdown starts
    for count in ["3", "2", "1", "GO!"]:
        if buttonA.justPressed():
            game["rocket_velocity"] = boost_strength
        update_rocket(game) 
        update_pipes(game)
        draw_game(game) 
        text_x = 30 
        text_y = 15 
        display.drawText(count, text_x, text_y, display.WHITE)
        display.update()

        # Delay to make the countdown readable
        for i in range(50000): 
            pass 
        
        # Erase the previous number by drawing black over
        display.drawText(count, text_x, text_y, display.BLACK)
        
    # Erase the final "GO!" text
    display.drawText("GO!", 30, 15, display.BLACK)
    display.update()
    wait_for_button_release() # Resume game
    return 

def main():
    while True:
        wait_for_button_release()
        draw_start_screen()
        while True:
            if buttonA.justPressed():
                break   # Start game
            if buttonB.justPressed():
                return  # Quit entire program
        game = new_game()
        
        # Initial Countdown Loop (3, 2, 1, GO!)
        for count in ["3", "2", "1", "GO!"]:
            if buttonA.justPressed():
                game["rocket_velocity"] = boost_strength
            update_rocket(game)
            update_pipes(game)
            draw_game(game) 
            text_x = 30 
            text_y = 15 
            display.drawText(count, text_x, text_y, display.WHITE)
            display.update()

            # Delay to make the countdown readable
            for i in range(50000): 
                pass 
            
            # Erase the previous number by drawing black over it
            display.drawText(count, text_x, text_y, display.BLACK)

        # Full Game Start
        game["started"] = True # Allows pipes to start moving
        
        # Erase the final "GO!" text
        display.drawText("GO!", text_x, text_y, display.BLACK)
        display.update()

        # Main Game Loop
        while game["running"]:
            if buttonA.justPressed():
                game["rocket_velocity"] = boost_strength

            # Pause Check (Button B)
            if buttonB.justPressed():
                pause_screen(game)
            update_rocket(game)
            update_pipes(game)
            draw_game(game)

        # Game Over
        choice = game_over_screen(game["score"])
        if choice == "quit":
            return
main()