from datetime import datetime, date

from django.http import HttpResponse
from django.shortcuts import render
from .models import Question, Answer, TestingCategory, TestingPeople, AnswerPeople
from our_school.models import User

def test_questions(request, slug_category_test):

    user = User.objects.get(id=request.user.pk)
    test_cat=TestingCategory.objects.filter(slug=slug_category_test).values()[0]['id']
    my_test = TestingPeople.objects.filter(people=user.id).filter(test=test_cat).values()[0]





    test = TestingCategory.objects.filter(slug=slug_category_test).values()[0]['id']
    quests = Question.objects.filter(testing_category_id=test)
    test_name =TestingCategory.objects.filter(slug=slug_category_test).values()[0]['name']


    answer = []
    for i in quests.values():
        answer1 = Answer.objects.filter(question_id=i['id'])

        answer += answer1

    return quests, test_name, test, answer

def testing(request, slug_category_test):
    username = request.user.username
    user = User.objects.get(id=request.user.pk)
    test_cat=TestingCategory.objects.filter(slug=slug_category_test).values()[0]['id']
    my_test = TestingPeople.objects.filter(people=user.id).filter(test=test_cat).values()[0]
    #print(my_test)
    testing_people = None
    #for i in my_test:
     #   if i.switch1 == True or i.switch2 == True:
      #      testing_people=i

    #if testing_people == None:
     #   return render(request, '1.html')

    test = TestingCategory.objects.filter(slug=slug_category_test).values()[0]['id']
    quests = Question.objects.filter(testing_category_id=test).order_by('?')
    test_name =TestingCategory.objects.filter(slug=slug_category_test).values()[0]['name']


    answer = []
    for i in quests.values():
        answer1 = Answer.objects.filter(question_id=i['id'])

        answer += answer1


    return render(request,'testing.html',{'quests': quests, 'answer': answer, 'name': username, 'test': test, 'test_name': test_name})

def answer(request,  slug_category_test):

    m = {}
    sum = 0
    people_answer = []
    username = request.user.username


    quests, test_name, test, answer2 = test_questions(request, slug_category_test)

    if len(request.POST) == 1:
        print(1)
        user = User.objects.get(username=username)
        test_category = TestingCategory.objects.filter(id=1).values()
        test_people_test = TestingPeople.objects.get(test_id=test_category[0]['id'], people=user.id)

        test_people_test.attempt = sum
        test_people_test.col -= 1
        test_people_test.save()

        return render(request, 'point.html',{'quests': quests, 'answer': answer2, 'name': username, 'test': test, 'test_name': test_name, "people_answer": people_answer})
    else:

        for i in request.POST:
            if i == 'csrfmiddlewaretoken':
                continue

            question = Question.objects.filter(id=i).values()

            test_category = TestingCategory.objects.filter(id=question[0]['testing_category_id']).values()
            s = []
            r = 0
            all_answer = 0
            #print(request.POST.getlist(i))
            for j in request.POST.getlist(i):
                people_answer.append(int(j))
                a = Answer.objects.filter(id=j).values()

                if a[0]['right'] == True:
                    r += 1
                all_answer += 1
            x = question[0]['num_right']


            if r == x and r == all_answer:
                ball = 1
            elif r == 1 and x == 2:
                ball = 0.5
            else:
                ball = 0
            sum += ball
            m[question[0]['text']] = ball
        #print(sum)
        #print(test_category)
        user = User.objects.get(username=username)



    test_people_test = TestingPeople.objects.filter(test_id=test_category[0]['id'], people= user.id)[0]
    #print(test_people_test.col)
    if test_people_test.col != 0:
        if sum < 9:
            test_people_test.attempt = sum
            test_people_test.col -=1
            test_people_test.save()
        else:
            test_people_test.attempt = sum
            test_people_test.col = 0
            test_people_test.att = True
            test_people_test.save()



    #             test_people_test.switch1 = False
    #             if test_people_test.attempt1 >= 9:
    #                 test_people_test.attempt2 = sum
    #             test_people_test.save()
    #
    #         elif test_people_test.switch2 == True:
    #             test_people_test.attempt2 = sum
    #             test_people_test.switch2 = False
    #             test_people_test.save()



    # if len(request.POST) == 1:
    #
    #     user = User.objects.get(username=username)
    #     test_category = TestingCategory.objects.filter(id=1).values()
    #     test_people_test = TestingPeople.objects.get(test_id=test_category[0]['id'], people=user.id)
    #     if test_people_test.switch1 == True:
    #         test_people_test.attempt1 = 0
    #         test_people_test.switch1 = False
    #         if test_people_test.attempt1 >= 9:
    #             test_people_test.attempt2 = sum
    #         test_people_test.save()
    #
    #     elif test_people_test.switch2 == True:
    #         test_people_test.attempt2 = 0
    #         test_people_test.switch2 = False
    #         test_people_test.save()
    #
    #     return render(request, 'point.html',{'quests': quests, 'answer': answer2, 'name': username, 'test': test, 'test_name': test_name, "people_answer": people_answer})
    # else:
    #     for i in request.POST:
    #         if i == 'csrfmiddlewaretoken':
    #             continue
    #
    #         question = Question.objects.filter(id=i).values()
    #
    #         test_category = TestingCategory.objects.filter(id=question[0]['testing_category_id']).values()
    #         s = []
    #         r = 0
    #         all_answer = 0
    #         #print(request.POST.getlist(i))
    #         for j in request.POST.getlist(i):
    #             people_answer.append(int(j))
    #             a = Answer.objects.filter(id=j).values()
    #
    #             if a[0]['right'] == True:
    #                 r += 1
    #             all_answer += 1
    #         x = question[0]['num_right']
    #
    #
    #         if r == x and r == all_answer:
    #             ball = 1
    #         elif r == 1 and x == 2:
    #             ball = 0.5
    #         else:
    #             ball = 0
    #         sum += ball
    #         m[question[0]['text']] = ball
    #     print(sum)
    #     #print(test_category)
    #     user = User.objects.get(username=username)
    #
    #
    #
    #     test_people_test = TestingPeople.objects.get(test_id=test_category[0]['id'], people= user.id)
    #     #print(test_people_test)
    #
    #     if test_people_test.switch1 == True:
    #         test_people_test.attempt1 = sum
    #         test_people_test.switch1 = False
    #         if test_people_test.attempt1 >= 9:
    #             test_people_test.attempt2 = sum
    #         test_people_test.save()
    #
    #     elif test_people_test.switch2 == True:
    #         test_people_test.attempt2 = sum
    #         test_people_test.switch2 = False
    #         test_people_test.save()

    #return render(request, 'base.html')

    # a = render(request, 'point.html',{'quests': quests, 'answer': answer2, 'name': username, 'test': test, 'test_name': test_name, "people_answer": people_answer})
    # test_file = open('test.html', 'w', encoding="utf-8")
    # b = a.content.decode('utf-8')
    # test_file.write(str(b))

    # print(quests)
    # print('-----------------------------')
    # print(answer2)
    # print('-----------------------------')
    # print(test)
    # print('-----------------------------')
    # print(test_name)
    # print('-----------------------------')
    # print(people_answer)

    with open(f'media/answer_text/{username}_{test_name}_{str(date.today())}_{datetime.now().strftime("%H-%M-%S")}.txt', 'a+') as text:
        #print(f'{username}_{test_name}_{datetime.now()}')
        text.write(test_name +'\n')
        text.write('_______________________________')
        for i in quests:
            if i.testing_category_id == test:
                text.write('\n' + str(i)+'\n')
            for j in answer2:
                if j.question_id == i.id:
                    if j.id in people_answer:
                        if j.right == False:
                            text.write(str(j) + ' - не правильно'+'\n')
                            print(str(j) + ' - не правильно')
                            continue
                        elif j.right == True:
                            text.write(str(j) + ' - правильно'+'\n')
                            print(str(j) + ' - правильно')
                            continue
                    text.write(str(j)+'\n')
                    print(str(j))
            text.write('_______________________________'+'\n')



    save_in_model = AnswerPeople.objects.create(test=test_name, people=username, document=f'answer_text/{username}_{test_name}_{str(date.today())}_{datetime.now().strftime("%H-%M-%S")}.txt')


    return render(request, 'point.html',{'quests': quests, 'answer': answer2, 'name': username, 'test': test, 'test_name': test_name, "people_answer": people_answer})

def index(request):
    username = request.user.username
    #category = TestingCategory.objects.filter(name="Напитки").values()[0]['id']
    category = TestingCategory.objects.all()
    #print(category)

    #quests = Question.objects.filter(testing_category_id=category)
    quests = Question.objects.all()
    answer=[]
    for i in quests.values():

        answer1 = Answer.objects.filter(question_id=i['id'])

        answer+=answer1
    #print(answer)
    #answer = Answer.objects.all
    return render(request, 'testing.html',{'quests': quests, 'answer': answer, 'name': username, 'category': category})

def answer1(request):
    m = {}
    sum = 0
    username = request.user.username
    #print(username)
    #request.POST.getlist('1')
    #print(request.POST)

    for i in request.POST:
        if i == 'csrfmiddlewaretoken':
            continue
        #print(i)
        #print(request.POST.getlist(i))
        q = Question.objects.filter(id=i).values()
        #print(q[0]['text'])
        #print(q[0]['num_right'])
        s=[]
        r=0
        all_answer=0
        for j in request.POST.getlist(i):
            a = Answer.objects.filter(id=j).values()
            #print(a[0]['right'])
            #s.append(a[0]['right'])

            if a[0]['right'] == True:
                r += 1
                #print(r)
            all_answer+=1

        x =q[0]['num_right']
        #print(r,x,all_answer)

        if r == x and r == all_answer:
            ball = 1
        elif r == 1 and x == 2:
            ball = 0.5
        else:
            ball = 0
        sum += ball
        m[q[0]['text']]=ball

    #print(m)
    #print(sum)


    user= User.objects.get(id=request.user.pk)
    user.point = sum
    user.number_attempts -=1
    if user.number_attempts == 0:
        user.turn_on_test = False


    user.save()

    #for i in request.POST:
     #   if i == 'csrfmiddlewaretoken':
      #      continue
       # a = Answer.objects.filter(id=i)

        #print(i)

        #b = [item.question_id for item in a][0]
        #print(b)
        #c = Question.objects.filter(id=b)
        #print(c)



    return render(request, 'point.html',{'name':username, 'ball':sum})

    #return HttpResponse(f"<h2>Name: {name}  Age: {age}</h2>")
