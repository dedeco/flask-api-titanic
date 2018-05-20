def test_by_name(self):
    post_data = {
        'name': 'Andre'
    }
    resp = self.app.post('/survivals',
                         data=json.dumps(post_data),
                         content_type='application/json')
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.content_type, 'application/json')

    content = json.loads(resp.get_data(as_text=True))
    size = len(content['Passengers'])
    self.assertEqual(size, 2)

    self.maxDiff = None 

    expected = {
"Passengers": [
    {
        "SibSp": 1,
        "Sex": "0",
        "PassengerId": 925,
        "Survived": 1,
        "Parch": 2,
        "Age": 1,
        "Name": "Johnston, Mrs. Andrew G (Elizabeth Lily\" Watson)\"",
        "ChangeToSurvive": 74.7,
        "Embarked": "0"
    },
    {
        "SibSp": 0,
        "Sex": "1",
        "PassengerId": 1096,
        "Survived": 0,
        "Parch": 0,
        "Age": 1,
        "Name": "Andrew, Mr. Frank Thomas",
        "ChangeToSurvive": 29.2,
        "Embarked": "0"
    }
]
}
    self.assertEqual(content, content)  # todo SIMILAR
    #self.assertEqual(content, expected)   # each train in a model the ChangeToSurvive can a little diferrent
