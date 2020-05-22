<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>{{name}}</h1>
        <hr />
        <br />
        <br />

        <v-select :options="subjects" @input="getClassTitles" />
        <v-select multiple v-if="class_titles.length" :options="class_titles" @input="getClassSections" label="title" />

        <div></div>
        <br />
        <br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">CRN</th>
              <th scope="col">Course</th>
              <th scope="col">Days</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(c, index) in schedule" :key="index">
              <td>{{ c.crn }}</td>
              <td>{{ c.title }}</td>
              <td>{{ c.days }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-success btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      schedule: [],
      name: '',
      id: '',
      subjects: [],
      class_titles: [],
      saved_classes: [],
      saved_sections: [],
      subject: '',
    };
  },
  methods: {
    getSchedule() {
      const path = 'http://localhost:5000/builder';
      axios
        .get(path)
        .then((res) => {
          this.schedule = res.data.schedule;
          this.name = res.data.name;
          this.id = res.data.id;
          this.subjects = res.data.subjects;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getClassTitles(subject) {
      const path = 'http://localhost:5000/builder';
      axios
        .post(path, { subject, goal: 'titles' })
        .then((res) => {
          this.getSchedule();
          this.subject = subject;
          this.class_titles = res.data.class_titles;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getClassSections(classTitle) {
      const path = 'http://localhost:5000/builder';
      // alert(this.subject);
      axios
        .post(path, { classTitle, goal: 'sections', subject: this.subject })
        .then((res) => {
          this.getSchedule();
          console.log(res.data.sections);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getSchedule();
  },
};
</script>
