# edit by Linn

def traverse(t):
    try:
        t.label()
    except AttributeError:
        print("not a label", t)
    else:
        its_gpe = False
        # Now we know that t.node is defined
        print('(', t.label())
        if t.label()=="GPE":
            print "!!"
            its_gpe = True
        else:
            its_gpe = False

        for child in t:
            if its_gpe: 
                print "This is a GPE child"
                print child[0]
            traverse(child)
        print(')')
