#function which collects all continents in the file in the order they appear
def continents(topUni, capitals):
    list = []
    topUni.seek(0, 0)
    count = 0
    count2 = 0

    #for each line read in the TopUni.csv file, the capitals.csv file is read again and looks for continents not already in the list
    for line in topUni:
        if count > 0:
            entries = line.split(",")
            COUNTRY = entries[2]
            for line in capitals:
                if count2 > 0:
                    entries2 = line.split(",")
                    CONTINENT = entries2[5].upper().rstrip("\n")
                    if COUNTRY.upper() in line or COUNTRY.title() in line:
                        if CONTINENT not in list:
                            list.append(CONTINENT)
                count2 += 1
            capitals.seek(0, 0)

        count += 1

    return list

#finds the continent the country is in and its capital and puts it into a list
def continentInfo(capitals, country):
    count = 0
    list = []
    capitals.seek(0, 0)

    #for loop which searches for the line with the selected country and its respective continent in it
    for line in capitals:
        if count > 0:
            entries = line.split(",")
            CONTINENT = entries[5].upper().rstrip("\n")
            if country.upper() in line or country.title() in line:
                selCont = CONTINENT
                capital = entries[1].upper()
                list.append(selCont)
                list.append(capital)

        count += 1

    return list

#finds all countries in the selected continent
def country_continents(capitals, continent):
    capitals.seek(0, 0)
    list = []
    for line in capitals:
        entries = line.split(",")
        if continent[0].title() in line:
            list.append(entries[0].upper())

    return list

#finds the score of all universities in the continent
def scores (topUni, contCountries):
    topUni.seek(0, 0)
    list = []
    for line in topUni:
        entries = line.split(",")
        COUNTRY = entries[2].upper()
        if COUNTRY in contCountries:
            list.append(float(entries[8]))

    return list

#calculates the continent relative score
def relativeScore(topUni, contCountries, average, continentScores):
    score = (average / continentScores[0]) * 100
    return int(score * 100) / 100

#find universities which contain the capital's name in its name
def findCapUnis(topUni, capital):
    topUni.seek(0, 0)
    list = []
    for line in topUni:
        entries = line.split(",")
        if capital[1].title() in line:
            list.append(entries[1].upper())

    return list

#main function
def getInformation(selectedCountry, topUni, capitals):
    try:
        #variables assigned to open the files
        universities = open(topUni, "r", encoding='utf8')
        geography = open(capitals, "r", encoding='utf8')
        outfile = open("output.txt", "w", encoding='utf8')

        #variables which account for the number of universities, all countries in the list, the score of all universities in the specified country, the number of universities, and their names respectively
        Num_of_Universities = -1
        countryList = []
        totalScore = 0
        universityCount = 0
        allUnis = []

        #for loop which reads each line in TopUni.csv
        for line in universities:
            if Num_of_Universities > -1:
                entries = line.split(",") #splits each line into a list with "," in-between them

                #constants which represent specific elements in each line
                NATIONAL = int(entries[3])
                RANK = int(entries[0])
                COUNTRY = entries[2].upper()
                UNIVERSITY = entries[1].upper()

                #appends the country into the countries list
                if COUNTRY not in countryList:
                    countryList.append(COUNTRY)

                #if the selected country is found in the line, the uni is placed into the list of unis in the country and its score is added to the total.
                if selectedCountry.title() in line or selectedCountry.upper() in line:
                    if NATIONAL == 1:
                        nationalTop = UNIVERSITY
                    allUnis.append(RANK)
                    allUnis.append(entries[1].upper())
                    totalScore += float(entries[8])
                    universityCount += 1

            Num_of_Universities += 1

        #variables which stores the average score of all universities in the country
        averageScore = int((totalScore / universityCount) * 100) / 100

        #function which collects all continents in the file in the order they appear
        continentList = continents(universities, geography)

        #finds the continent the country is in and its capital and puts it into a list
        Continent_Capital = continentInfo(geography, selectedCountry)

        #finds all countries in the selected continent
        continentCountries = country_continents(geography, Continent_Capital)

        #finds the score of all universities in the continent
        allScores = scores(universities, continentCountries)

        #calculates the continent relative score
        continentScore = relativeScore(universities, continentCountries, averageScore, allScores)

        #find universities which contain the capital's name in its name
        capitalUnis = findCapUnis(universities, Continent_Capital)

        #series of functions which writes the information out in the output file
        outfile.write("Total number of universities => {}".format(Num_of_Universities))
        outfile.write("\n\nAvailable countries => {}".format(", ".join(countryList)))
        outfile.write("\n\nAvailable continents => {}".format(", ".join(continentList)))
        outfile.write("\n\nAt international rank => {} the university name is => {}".format(allUnis[0], allUnis[1]))
        outfile.write("\n\nAt national rank => 1 the university name is => {}".format(nationalTop))
        outfile.write("\n\nThe average score => {:.2f}".format(averageScore))
        outfile.write("\n\nThe relative score to the top university in {} is => ({:.2f} / {:.2f}) x 100% = {:.2f}%".format(Continent_Capital[0], averageScore, allScores[0], continentScore))
        outfile.write("\n\nThe capital is => {}".format(Continent_Capital[1]))
        outfile.write("\n\nThe universities that contain in the capital name =>")
        position = 1
        for unis in capitalUnis:
            outfile.write("\n\t#{} {}".format(position, unis))
            position += 1

    #exception to detect the error
    except FileNotFoundError:
        outfile = open("output.txt", "w")
        outfile.write("Error: file not found")

    #finally statement to close all the files opened
    finally:
        universities.close()
        geography.close()
        outfile.close()

#calls the main function
getInformation("usa", "TopUni.csv", "capitals.csv")
