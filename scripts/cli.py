import qa

if __name__ =="__main__":
    while(True):
        text = input("Enter question:\n")
        if text.lower() == 'more info' and counter < len(sim):
            #print("Counter=", counter)
            ansr = expl[sim.index(max_sim[counter])]
            #print("Answer=", ansr)
            counter += 1
            response = ansr + "\nIf you want to know more, type \"More info\"."
            print(response)
        elif text.lower() != 'more info':
            counter = 1
            expl, sim, max_sim = qa.generate_response(text)
            if expl:
                ansr = expl[sim.index(max_sim[0])]
                #print("Answer 1st =", ansr)
                response = ansr + "\nIf you want to know more, type \"More info\"."
                print(response)
            else:
                response = "Sorry, I don't know about that!"
        else:
            print("That's all the information we've got. Sorry!")
