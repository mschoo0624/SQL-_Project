
# Name: Minseo Choo
# UIN: 664433243
# NetID: mchoo2
import sqlite3
import matplotlib.pyplot as figure
import datetime # for the command 8

##################################################################
# print_stats
#
# Given a connection to the database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General Statistics:")
    
    dbCursor.execute("SELECT COUNT(*) FROM RedCameras;")
    row = dbCursor.fetchone()   
    print("  Number of Red Light Cameras:", f"{row[0]:,}")
    
    # for other general informations (My Work)
    dbCursor.execute("SELECT COUNT(*) FROM SpeedCameras;")
    row = dbCursor.fetchone() 
    print("  Number of Speed Cameras:", f"{row[0]:,}")
    
    dbCursor.execute("SELECT COUNT(*) FROM RedViolations;")
    row = dbCursor.fetchone() 
    print("  Number of Red Light Camera Violation Entries:", f"{row[0]:,}")
    
    dbCursor.execute("SELECT COUNT(*) FROM SpeedViolations;")
    row = dbCursor.fetchone() 
    print("  Number of Speed Camera Violation Entries:", f"{row[0]:,}")
    
    dbCursor.execute("SELECT MIN(Violation_Date), MAX(Violation_Date) FROM SpeedViolations;")
    row = dbCursor.fetchone() 
    print(f"  Range of Dates in the Database: {row[0]} - {row[1]}")
    
    dbCursor.execute("SELECT SUM(Num_Violations) AS TotalSum FROM RedViolations;")
    row = dbCursor.fetchone() 
    print("  Total Number of Red Light Camera Violations:", f"{row[0]:,}")
    
    dbCursor.execute("SELECT SUM(Num_Violations) AS TotalSum FROM SpeedViolations;")
    row = dbCursor.fetchone() 
    print("  Total Number of Speed Camera Violations:", f"{row[0]:,}")
    # Done
    
# Function for Option 1:
def option1(dbConn):
    print()
    name = input("Enter the name of the intersection to find (wildcards _ and % allowed): ")
    
    name = name.replace('*', '%') # Replace * with % for SQL LIKE operator
    
    dbCursor = dbConn.cursor()
    
    # Creaeting the SQLite code functionality. 
    sql = """ 
    SELECT Intersection_ID, Intersection
    FROM intersections
    WHERE Intersection LIKE ?
    ORDER BY Intersection;
    """
    
    dbCursor.execute(sql, (name,))
    rows = dbCursor.fetchall()

    if rows: # if the name input exists in the SQL code. 
        for row in rows:
            print(f"{row[0]} : {row[1]}")
    else:
        print("No intersections matching that name were found.")
    print()
        
# Function for Option 2
def option2(dbConn):
    print()  # Add line break after menu choice
    name = input("Enter the name of the intersection (no wildcards allowed): ")
    print()  # Add line break after input
    
    dbCursor = dbConn.cursor()
    
    # Red light intersection code
    red_light = """
    SELECT RedCameras.Camera_ID, RedCameras.Address
    FROM RedCameras 
    JOIN Intersections ON RedCameras.Intersection_ID = Intersections.Intersection_ID
    WHERE Intersections.Intersection = ?
    ORDER BY RedCameras.Camera_ID ASC;
    """

    # Speed camera intersection code
    speed_camera = """
    SELECT SpeedCameras.Camera_ID, SpeedCameras.Address
    FROM SpeedCameras 
    JOIN Intersections ON SpeedCameras.Intersection_ID = Intersections.Intersection_ID
    WHERE Intersections.Intersection = ?
    ORDER BY SpeedCameras.Camera_ID ASC;
    """

    # Execute the Red Light Camera sql code
    dbCursor.execute(red_light, (name,))
    red_light_rows = dbCursor.fetchall()

    if red_light_rows:
        print("Red Light Cameras:")
        for row in red_light_rows:
            print(f"    {row[0]} : {row[1]}")
    else:
        print("No red light cameras found at that intersection.")

    print()  # Add line break between sections

    # Execute the Speed Camera sql code
    dbCursor.execute(speed_camera, (name,))
    speed_camera_rows = dbCursor.fetchall()

    if speed_camera_rows:
        print("Speed Cameras:")
        for row in speed_camera_rows:
            print(f"    {row[0]} : {row[1]}")
    else:
        print("No speed cameras found at that intersection.")

    print()   

# Function for Option 3
def option3(dbConn):
    print()
    date = input("Enter the date that you would like to look at (format should be YYYY-MM-DD): ").strip() # Using strip just in case to remove leading char from the string
    
    dbCursor = dbConn.cursor()
    
    # Creating the sql code for check if the Violation date exists. 
    datecheck = """
    SELECT RedViolations.Violation_Date
    FROM RedViolations
    JOIN SpeedViolations 
    ON RedViolations.Violation_Date = SpeedViolations.Violation_Date
    WHERE RedViolations.Violation_Date LIKE ?
    """
    
    dbCursor.execute(datecheck, (date,))
    check = dbCursor.fetchone()
    
    # Debugging the if the date is valid or invalid.
    if not check: 
        print("No violations on record for that date.\n")
        return
    
    # Getting the Number of Red Light Violations
    Red_light_violations = """
    SELECT SUM(Num_Violations) AS Total
    FROM RedViolations
    WHERE Violation_Date = ?
    """
   
    dbCursor.execute(Red_light_violations, (date,))
    red_light_rows = dbCursor.fetchone()
    num1 = red_light_rows[0]
    
    ###########################################################################
    
    # Getting the Number of Speed Violations
    Speed_Violations = """
    SELECT SUM(Num_Violations) AS Total
    FROM SpeedViolations
    WHERE Violation_Date = ?
    """
    
    dbCursor.execute(Speed_Violations, (date,))
    speed_rows = dbCursor.fetchone()
    num2 = speed_rows[0]
    
    total = num1 + num2
    Red_percent = (num1 / total) * 100
    Speed_percent = (num2 / total) * 100
    
    print("Number of Red Light Violations:", f"{num1:,}", f"({Red_percent:.3f}%)")
    print("Number of Speed Violations:", f"{num2:,}", f"({Speed_percent:.3f}%)")
    print("Total Number of Violations:", f"{total:,}")
    print()
    
def option4(dbConn):
    print()
    dbCursor = dbConn.cursor()
    
    red_camera = """
    SELECT Intersections.Intersection, Intersections.Intersection_ID, 
    COUNT(RedCameras.Intersection_ID) AS EachTotal
    FROM Intersections
    JOIN RedCameras 
    ON Intersections.Intersection_ID = RedCameras.Intersection_ID
    GROUP BY Intersections.Intersection, Intersections.Intersection_ID
    ORDER BY EachTotal DESC, Intersections.Intersection_ID DESC;
    """
    
    dbCursor.execute(red_camera)
    red_row = dbCursor.fetchall()
    
    red_query = "SELECT COUNT(*) FROM RedCameras"
    dbCursor.execute(red_query)
    total_red = dbCursor.fetchone()[0]  
    
    if red_row:
        print("Number of Red Light Cameras at Each Intersection")
        
        for row in red_row:
            red_num = row[2]  
            red_percent = (red_num / total_red) * 100 
            print(f"   {row[0]} ({row[1]}) : {row[2]} ({red_percent:.3f}%)")
            
    print()
    
    #same process but, for the speed camera
    ####################################################################################
    
    speed_camera = """
    SELECT 
    Intersections.Intersection, 
    Intersections.Intersection_ID, 
    COUNT(SpeedCameras.Intersection_ID) AS EachTotal
    FROM Intersections
    JOIN SpeedCameras 
    ON Intersections.Intersection_ID = SpeedCameras.Intersection_ID
    GROUP BY Intersections.Intersection, Intersections.Intersection_ID
    ORDER BY EachTotal DESC, Intersections.Intersection_ID DESC;
    """ 

    dbCursor.execute(speed_camera)
    speed_row = dbCursor.fetchall()

    speed_query = "SELECT COUNT(*) FROM SpeedCameras"
    dbCursor.execute(speed_query)
    total_speed = dbCursor.fetchone()[0]  

    #Printing out Code. 
    if speed_row:
        print("Number of Speed Cameras at Each Intersection")
        for row in speed_row:
            speed_num = row[2]  
            speed_percent = (speed_num / total_speed) * 100  
            print(f"  {row[0]} ({row[1]}) : {row[2]} ({speed_percent:.3f}%)")
            
    print()
            
def option5(dbConn):
    print()
    date = input("Enter the year that you would like to analyze: ").strip()
    print()
    dbCursor = dbConn.cursor()

    # Red Light Violations Query
    red_violations = """
    SELECT 
        Intersections.Intersection,
        Intersections.Intersection_ID,
        SUM(RedViolations.Num_Violations) AS TotalViolations
    FROM Intersections
    JOIN RedCameras ON Intersections.Intersection_ID = RedCameras.Intersection_ID
    JOIN RedViolations ON RedCameras.Camera_ID = RedViolations.Camera_ID
    WHERE strftime('%Y', RedViolations.Violation_Date) = ?
    GROUP BY Intersections.Intersection, Intersections.Intersection_ID
    ORDER BY TotalViolations DESC, Intersections.Intersection_ID DESC;
    """
    
    dbCursor.execute(red_violations, (date,))
    red_row = dbCursor.fetchall()

    red_query = "SELECT SUM(Num_Violations) FROM RedViolations WHERE strftime('%Y', Violation_Date) = ?"
    dbCursor.execute(red_query, (date,))
    total_red = dbCursor.fetchone()[0]

    print(f"Number of Red Light Violations at Each Intersection for {date}")
    if red_row and total_red > 0:
        for row in red_row:
            red_num = row[2]
            red_percentage = (red_num / total_red) * 100
            print(f"  {row[0]} ({row[1]}) : {row[2]:,} ({red_percentage:.3f}%)")

        print(f"Total Red Light Violations in {date} : {total_red:,}")
    else: 
        print("No red light violations on record for that year.")

    print()

    # Speed Violations Query
    speed_violations = """
    SELECT 
        Intersections.Intersection,
        Intersections.Intersection_ID,
        SUM(SpeedViolations.Num_Violations) AS TotalViolations
    FROM Intersections
    JOIN SpeedCameras ON Intersections.Intersection_ID = SpeedCameras.Intersection_ID
    JOIN SpeedViolations ON SpeedCameras.Camera_ID = SpeedViolations.Camera_ID
    WHERE strftime('%Y', SpeedViolations.Violation_Date) = ?
    GROUP BY Intersections.Intersection, Intersections.Intersection_ID
    ORDER BY TotalViolations DESC, Intersections.Intersection_ID DESC;
    """
    
    dbCursor.execute(speed_violations, (date,))
    speed_row = dbCursor.fetchall()

    speed_query = "SELECT SUM(Num_Violations) FROM SpeedViolations WHERE strftime('%Y', Violation_Date) = ?"
    dbCursor.execute(speed_query, (date,))
    total_speed = dbCursor.fetchone()[0]

    print(f"Number of Speed Violations at Each Intersection for {date}")
    if speed_row and total_speed > 0:
        for row in speed_row:
            speed_num = row[2]
            speed_percentage = (speed_num / total_speed) * 100  
            print(f"  {row[0]} ({row[1]}) : {row[2]:,} ({speed_percentage:.3f}%)")

        print(f"Total Speed Violations in {date} : {total_speed:,}")
    else:
        print("No speed violations on record for that year.")
   
def option6(dbConn):
    print()
    ID = input("Enter a camera ID: ")  
    
    dbCursor = dbConn.cursor()
    
    # using UNION ALL to merge results while maintaining all records.  
    #change
    violations = """
    SELECT Year, SUM(TotalViolations) as TotalViolations
    FROM (
        SELECT strftime('%Y', Violation_Date) AS Year, Num_Violations as TotalViolations
        FROM RedViolations 
        WHERE Camera_ID LIKE ?
        
        UNION ALL
        
        SELECT strftime('%Y', Violation_Date) AS Year, Num_Violations as TotalViolations
        FROM SpeedViolations 
        WHERE Camera_ID LIKE ?
    ) combined
    GROUP BY Year
    ORDER BY Year ASC;
    """

    dbCursor.execute(violations, (ID, ID))
    violation_rows = dbCursor.fetchall()
    
    x = [] #year
    y = [] #violations
    
    if violation_rows:
        print(f"Yearly Violations for Camera {ID}")  
        for row in violation_rows:
            print(f"{row[0]} : {row[1]:,}")
            x.append(row[0])
            y.append(row[1])
    else: 
        print("No cameras matching that ID were found in the database.\n")
        return
        
    Choice = input("Plot? (y/n) ")
    
    if Choice == 'n':
        return
    elif Choice == 'y':
        figure.plot(x, y, color='blue')
        figure.xlabel("Year")
        figure.ylabel("Number of Violations")
        figure.title(f"Yearly Violations for Camera {ID}")
        figure.show()
        return
    else:
        return
    
    print()

def option7(dbConn):
    print()
    ID = input("Enter a camera ID: ")
    
    dbCursor = dbConn.cursor()
    
    #Since I need to check the Camera_ID before entering the year input. 
    dbCursor.execute( """ 
    SELECT COUNT(*) FROM (
        SELECT Camera_ID FROM RedViolations WHERE Camera_ID LIKE ?
        UNION
        SELECT Camera_ID FROM SpeedViolations WHERE Camera_ID LIKE ?
    ) AS CameraCheck;
    """, (ID, ID))
    
    CameraCheck = dbCursor.fetchone()

    if CameraCheck[0] == 0: # Handling the Camera_ID is found or not.
        print("No cameras matching that ID were found in the database.")
        return
    
    Year = input("Enter a year: ")
    
    sql_code = """
    SELECT Date, SUM(TotalViolations) AS TotalViolations
    FROM (
        SELECT strftime('%m', Violation_Date) AS Date, Num_Violations AS TotalViolations
        FROM RedViolations
        WHERE Camera_ID LIKE ? AND strftime('%Y', Violation_Date) LIKE ?
        
        UNION ALL 
        
        SELECT strftime('%m', Violation_Date) AS Date, Num_Violations AS TotalViolations
        FROM SpeedViolations
        WHERE Camera_ID LIKE ? AND strftime('%Y', Violation_Date) LIKE ?
    ) AS Combined
    GROUP BY Date
    ORDER BY Date ASC;
    """
    
    # need (ID, Year, ID, Year)) since it should take the input for Red and Speed Violations separately
    dbCursor.execute(sql_code, (ID, Year, ID, Year))
    rows = dbCursor.fetchall()
    
    x = [] #month
    y = [] #violations
    
    print(f"Monthly Violations for Camera {ID} in {Year}")
    if rows:
        for row in rows:
            print(f"{row[0]}/{Year} : {row[1]:,}")
            x.append(row[0]) # appending the months 
            y.append(row[1]) # appending the number of violations
    
    choice = input("Plot? (y/n) ")
    
    if choice == 'y':
        figure.plot(x, y, color='blue')
        figure.xlabel("Month")
        figure.ylabel("Number of Violations")
        figure.title(f"Monthly Violations for Camera {ID} ({Year})")
        figure.show()
    else:
        return
    
    print()

def option8(dbConn):
    print()
    year = input("Enter a year: ")
    
    dbCursor = dbConn.cursor()
    
    RedLight = """
    SELECT Violation_Date, SUM(Num_Violations) AS Total
    FROM RedViolations
    WHERE strftime('%Y', Violation_Date) LIKE ?
    GROUP BY Violation_Date
    ORDER BY Violation_Date ASC;
    """
    
    dbCursor.execute(RedLight, (year,))
    redrows = dbCursor.fetchall()
    
    RedDate = [] #month
    RedViolations = [] #violations
    
    print("Red Light Violations:")
    if redrows:
        Redfirst5 = redrows[:5]  # First 5 days
        Redlast5 = redrows[-5:]  # Last 5 days

        for row in Redfirst5 + Redlast5:  # Print first and last 5 days
            print(f"{row[0]} {row[1]}")  
        for rows in redrows:
            RedDate.append(rows[0]) # appending for the graph plotting later on
            RedViolations.append(rows[1]) # appending for the graph plotting later on 
    
    Speed = """
    SELECT Violation_Date, SUM(Num_Violations) AS Total
    FROM SpeedViolations
    WHERE strftime('%Y', Violation_Date) LIKE ?
    GROUP BY Violation_Date
    ORDER BY Violation_Date ASC;
    """
    
    dbCursor.execute(Speed, (year,))
    speedrows = dbCursor.fetchall()
    
    SpeedDate = [] # month
    SpeedViolations = [] # violations
    
    print("Speed Violations:")
    if redrows:
        Speedfirst5 = speedrows[:5]  # First 5 days
        Speedlast5 = speedrows[-5:]  # Last 5 days

        for row in Speedfirst5 + Speedlast5:  # Print first and last 5 days
            print(f"{row[0]} {row[1]}")  
        for rows in speedrows:
            SpeedDate.append(rows[0]) # appending for the graph plotting later on
            SpeedViolations.append(rows[1]) # appending for the graph plotting later on 
    
    choice = input("Plot? (y/n) ")
    
    if choice == 'y':
        # Setting the date rangge from the input date. 
        start = datetime.date(int(year), 1, 1)
        end = datetime.date(int(year), 12, 31)
        all_days = [start + datetime.timedelta(days = i) for i in range((end - start).days + 1)]
        
        # Create dictionaries to map violations to dates
        red_dict = {datetime.datetime.strptime(date, "%Y-%m-%d").date(): count for date, count in zip(RedDate, RedViolations)}
        speed_dict = {datetime.datetime.strptime(date, "%Y-%m-%d").date(): count for date, count in zip(SpeedDate, SpeedViolations)}

        # Filling in the blanks with 0 violations guarantees that every day of the year is represented, even if there were no documented infractions.
        red = [red_dict.get(day, 0) for day in all_days]
        speed = [speed_dict.get(day, 0) for day in all_days]

        # Plot the data
        figure.plot(range(1, len(all_days) + 1), red, label="Red Light", color="red")
        figure.plot(range(1, len(all_days) + 1), speed, label="Speed", color="orange")

        # Formatting the plot
        figure.title(f"Violations Each Day of {year}")
        figure.xlabel("Day")
        figure.ylabel("Number of Violations")
        figure.show()
    else: 
        return
    
    print()
        
def option9(dbConn):
    print()
    Name = input("Enter a street name: ").strip()
    
    dbCursor = dbConn.cursor()
    
    RedCameras = """
    SELECT Camera_ID, Address, Latitude, Longitude
    FROM RedCameras
    WHERE Address LIKE ?
    GROUP BY Camera_ID
    ORDER BY Camera_ID ASC;
    """
    
    dbCursor.execute(RedCameras, (f"%{Name}%",))
    redrows = dbCursor.fetchall()
    
    SpeedCameras = """
    SELECT Camera_ID, Address, Latitude, Longitude
    FROM SpeedCameras
    WHERE Address LIKE ?
    GROUP BY Camera_ID
    ORDER BY Camera_ID ASC;
    """
    
    dbCursor.execute(SpeedCameras, (f"%{Name}%",))
    speedrows = dbCursor.fetchall()
    
    # Red Violations
    xRed = []
    yRed = []
    # Speed Violations
    xSpeed = []
    ySpeed = []
        
    if redrows or speedrows:
        print(f"\nList of Cameras Located on Street: {Name}")

        # Always print the section headers
        print("  Red Light Cameras:")
        if redrows:
            for row in redrows:
                print(f"     {row[0]} : {row[1]} ({row[2]}, {row[3]})")
                # Getting the Log & Lat
                xRed.append(row[2])
                yRed.append(row[3])
        
        print("  Speed Cameras:")
        if speedrows:
            for row in speedrows:
                print(f"     {row[0]} : {row[1]} ({row[2]}, {row[3]})")
                # Getting the Log & Lat
                xSpeed.append(row[2])
                ySpeed.append(row[3])
    else:
        print("There are no cameras located on that street.")
        return

    choice = input("\nPlot? (y/n) ")
    
    if choice == 'y':
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868]  # Area covered by the map
        image = figure.imread("chicago.png")  # Load image without extent
        figure.imshow(image, extent=xydims) 
        figure.title("Cameras on Street: " + Name)

        print(xRed)
        print(yRed)
        # Ensure variable names are consistent
        figure.plot(yRed, xRed, color='red', marker='o', linestyle='-', label='Red Light Cameras')
        figure.plot(ySpeed, xSpeed, color='orange', marker='o', linestyle='-', label='Speed Cameras')

        # Annotate each camera with its ID
        for row in redrows:
            figure.annotate(row[0], (row[3], row[2]), color='red', fontsize=9, fontweight='bold')
        for row in speedrows:
            figure.annotate(row[0], (row[3], row[2]), color='orange', fontsize=9, fontweight='bold')
 
        figure.xlim([-87.9277, -87.5569])
        figure.ylim([41.7012, 42.0868])
        figure.show()
    else: 
        return
##################################################################  
#
# main
#
dbConn = sqlite3.connect('chicago-traffic-cameras.db')

print("Project 1: Chicago Traffic Camera Analysis")
print("CS 341, Spring 2025")
print()
print("This application allows you to analyze various")
print("aspects of the Chicago traffic camera database.")
print()
print_stats(dbConn)
print()

while True: #Using the while true inorder to loop it.
    print()
    print("Select a menu option: ")
    print("  1. Find an intersection by name")
    print("  2. Find all cameras at an intersection")
    print("  3. Percentage of violations for a specific date")
    print("  4. Number of cameras at each intersection")
    print("  5. Number of violations at each intersection, given a year")
    print("  6. Number of violations by year, given a camera ID")
    print("  7. Number of violations by month, given a camera ID and year")
    print("  8. Compare the number of red light and speed violations, given a year")
    print("  9. Find cameras located on a street")
    print("or x to exit the program.")

    choice = input("Your choice --> ").strip()
    
    if choice == "x":
        print("Exiting program.")
        break
    elif choice == "1":
        option1(dbConn)
    elif choice == "2":
        option2(dbConn)
    elif choice == "3":
        option3(dbConn)
    elif choice == "4":
        option4(dbConn)
    elif choice == "5":
        option5(dbConn)
    elif choice == "6":
        option6(dbConn)
    elif choice == "7":
        option7(dbConn) 
    elif choice == "8":
        option8(dbConn)
    elif choice == "9":
        option9(dbConn)
    else:
        print("Error, unknown command, try again...")