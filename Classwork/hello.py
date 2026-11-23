counter = 1 
while counter <= 100:
    #print(counter)

    fizz = counter % 3 == 0
    buzz = counter % 5 == 0 

    if fizz:
        print(str(counter) +"fizz")
    if buzz: 
        print(str(counter)+ "buzz")

    counter = counter + 1
    if counter % 3 == 0:
        print(str(counter) + "fizz")
    if counter % 5 == 0:
        print (str(counter) + "buzz")
    if counter % 15 == 0: 
        print (str(counter) + "fizzbuzz")
        