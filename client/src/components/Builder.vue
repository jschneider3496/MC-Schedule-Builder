<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>{{name}}</h1>
        <hr />
        <br />
        <br />

        <v-select :options="subjects" @input="getClassTitles" />
        <v-select
          v-if="class_titles.length"
          :options="class_titles"
          @input="getClassSections"
          label="title"
        />

        <div v-for="(sections, title) in selected_titles" :key="title">
          <b-button v-b-toggle=title class="m-1">{{ title }}</b-button>
          <b-collapse :id="title" v-for="(x, index) in sections" :key="index">
            <b-card>{{ x.crn }}</b-card>
          </b-collapse>
        </div>

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
      // from schedule file
      schedule: [],
      name: '',
      id: '',
      selected_titles: {},

      // Temporary
      class_titles: [],
      saved_classes: [],
      saved_sections: [],
      subjects: [],
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
          this.selected_titles = res.data.selected_titles;
          console.log(this.selected_titles);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getClassTitles(subject) {
      const path = 'http://localhost:5000/builder';
      axios
        .post(path, { subject, goal: 'getTitles' })
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
        .post(path, { classTitle, goal: 'getSections', subject: this.subject })
        .then(() => {
          this.getSchedule();
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
