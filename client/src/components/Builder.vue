<template>
  <div class="container">
    <!-- Header -->
    <div>
      <b-navbar toggleable="lg" type="dark" variant="info">
        <b-navbar-brand href="#">MC Scheduler: {{name}}</b-navbar-brand>
      </b-navbar>
    </div>

    <b-container class="split-screen">
      <b-row>
        <!-- LHS of screen -->
        <b-col cols="12" md="8">
          <div class="row">
            <div class="col-sm-10">

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
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </b-col>

        <!-- RHS of screen -->
        <b-col cols="6" md="4">
          <!-- Select Subject -->
          <v-select :options="subjects" @input="getClassTitles" />
          <!-- Select course title -->
          <v-select
            v-if="class_titles.length"
            :options="class_titles"
            @input="getClassSections"
            label="title"
          />

          <!-- Select section -->
          <div v-for="(sections, title) in selected_titles" :key="title">
            <b-button v-b-toggle="title" class="m-1">{{ title }}</b-button>
            <b-collapse :id="title" v-for="(x, index) in sections" :key="index">
              <b-card>
                <div>{{x.course}}: {{ x.crn }}</div>
                <div>{{x.location}}: {{ x.campus }}</div>
                <div>
                  <!-- Select/Unselect course (will add and drop to schedule) -->
                  <b-form-checkbox-group
                    :id="x.crn"
                    v-model="schedule"
                    :options="[{text: x.crn, value: x}]"
                    @change="onCheckbox"
                  ></b-form-checkbox-group>
                </div>
              </b-card>
            </b-collapse>
            <!-- Remove selected course title -->
            <b-collapse :id="title">
              <b-card>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteSelectedTitle(title)"
                >Delete</button>
              </b-card>
            </b-collapse>
          </div>
        </b-col>
      </b-row>
    </b-container>
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
      if (classTitle != null) {
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
      }
    },
    onCheckbox(update) {
      this.updateSchedule(update);
    },
    updateSchedule(payload) {
      const path = `http://localhost:5000/builder/${this.id}`;
      axios
        .put(path, { payload, goal: 'updateSchedule' })
        .then(() => {
          this.getSchedule();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSchedule();
        });
    },
    onDeleteSelectedTitle(selectedTitle) {
      this.removeSelectedTitle(selectedTitle);
    },
    removeSelectedTitle(payload) {
      const path = `http://localhost:5000/builder/${this.id}`;
      axios
        .put(path, { payload, goal: 'removeSelectedTitle' })
        .then(() => {
          this.getSchedule();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSchedule();
        });
    },
  },
  created() {
    this.getSchedule();
  },
};
</script>
