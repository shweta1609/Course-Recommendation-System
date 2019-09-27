from flask import Flask, flash, render_template, request, session, url_for

import sys
sys.path.append("../ContentBasedCF")
sys.path.append("../ItemBasedCF")
sys.path.append("../PopularCourseRecommend")
sys.path.append("../UserBasedCF")
print(sys.path)
from contentbased import content_based_api
from itemBasedCF_API import itemBasedCF_API
from userBasedCF_API import userBasedCF_API
from popularCourseRecommend_API import popularCourseRecommend


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('course_selection.html')

@app.route("/newpage", methods=['GET','POST'])
def recommend_courses():
    course_list = {}
    course_attr = []
    recommendation = []
    if request.method == 'GET':
        return "something went wrong"
    else:
        i=1
        count = len(request.form)
        while i <= (count-1)/5:
            course_name = request.form['course'+str(i)]
            course_list[course_name] = []
            i += 1
        if request.form['action'] == 'ItemBasedCF':
            i=1
            count = len(request.form)
            while i <= (count-1)/5:
                course_name = request.form['course'+str(i)]

                difficulty = request.form['difficulty'+str(i)]
                if difficulty == "Very Hard":
                    course_attr.append(0)
                elif difficulty == "Hard":
                    course_attr.append(1)
                elif difficulty == "Medium":
                    course_attr.append(2)
                elif difficulty == "Easy":
                    course_attr.append(3)
                elif difficulty == "Very Easy":
                    course_attr.append(4)
                else:
                    course_attr.append(-100)

                like1 = request.form['like'+str(i)]
                if like1 == "Strongly Disliked":
                    course_attr.append(0)
                elif like1 == "Disliked":
                    course_attr.append(1)
                elif like1 == "Neutral":
                    course_attr.append(2)
                elif like1 == "Liked":
                    course_attr.append(3)
                elif like1 == "Loved!":
                    course_attr.append(4)
                else:
                    course_attr.append(-100)


                load1 = request.form['workload'+str(i)]
                if load1 == "very heavy":
                    course_attr.append(0)
                elif load1 == "heavy":
                    course_attr.append(1)
                elif load1 == "moderate":
                    course_attr.append(2)
                elif load1 == "light":
                    course_attr.append(3)
                elif load1 == "very light":
                    course_attr.append(4)
                else:
                    course_attr.append(-100)

                sentiment1 = request.form['sentiment'+str(i)]
                if sentiment1 == "Very negative":
                    course_attr.append(0)
                elif sentiment1 == "Negative":
                    course_attr.append(1)
                elif sentiment1 == "Neutral":
                    course_attr.append(2)
                elif sentiment1 == "Positive":
                    course_attr.append(3)
                elif sentiment1 == "Very positive":
                    course_attr.append(4)
                else:
                    course_attr.append(-100)

                course_list[course_name] = course_attr
                i += 1
            recommendation = itemBasedCF_API(course_list)
            print "abc"

        elif request.form['action'] == 'UserBasedCF':
            i=1
            count = len(request.form)
            while i <= (count-1)/5:
                course_name = request.form['course'+str(i)]

                difficulty = request.form['difficulty'+str(i)]
                if difficulty == "Very Hard":
                    course_attr.append(0)
                elif difficulty == "Hard":
                    course_attr.append(1)
                elif difficulty == "Medium":
                    course_attr.append(2)
                elif difficulty == "Easy":
                    course_attr.append(3)
                elif difficulty == "Very Easy":
                    course_attr.append(4)
                else:
                    course_attr.append(-100)
                    
                like1 = request.form['like'+str(i)]
                if like1 == "Strongly Disliked":
                    course_attr.append(0)
                elif like1 == "Disliked":
                    course_attr.append(1)
                elif like1 == "Neutral":
                    course_attr.append(2)
                elif like1 == "Liked":
                    course_attr.append(3)
                elif like1 == "Loved!":
                    course_attr.append(4)
                else:
                    course_attr.append(-100)


                load1 = request.form['workload'+str(i)]
                if load1 == "very heavy":
                    course_attr.append(0)
                elif load1 == "heavy":
                    course_attr.append(1)
                elif load1 == "moderate":
                    course_attr.append(2)
                elif load1 == "light":
                    course_attr.append(3)
                elif load1 == "very light":
                    course_attr.append(4)
                else:
                    course_attr.append(-100)

                sentiment1 = request.form['sentiment'+str(i)]
                if sentiment1 == "Very negative":
                    course_attr.append(0)
                elif sentiment1 == "Negative":
                    course_attr.append(1)
                elif sentiment1 == "Neutral":
                    course_attr.append(2)
                elif sentiment1 == "Positive":
                    course_attr.append(3)
                elif sentiment1 == "Very positive":
                    course_attr.append(4)
                else:
                    course_attr.append(-100)

                course_list[course_name] = course_attr
                i += 1
            recommendation = userBasedCF_API(course_list)

        elif request.form['action'] == 'ContentBased':
            recommendation = content_based_api(course_list)
            print course_list

        elif request.form['action'] == 'PopularCourse':
            recommendation = popularCourseRecommend()
            print "abc"

        return render_template('course_recommendation.html', course=recommendation)


if __name__ == "__main__":
    # app.debug = True
    app.run(host='127.0.0.1', port=80, threaded=True, debug=True)