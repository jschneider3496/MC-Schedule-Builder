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
          <v-expansion-panels multiple>
            <v-expansion-panel v-for="(sections, title) in selected_titles" :key="title">
              <v-expansion-panel-header outline :color="sections[0].class_color">
                {{title}}
                <template v-slot:actions>
                  <v-icon color="white">mdi-check</v-icon>
                </template>
              </v-expansion-panel-header>
              <v-expansion-panel-content :id="title" v-for="(x, index) in sections" :key="index">
                <v-card class="mx-auto" outlined>
                  <v-list-item three-line>
                    <v-list-item-content>
                      <v-container>
                        <v-row justify="space-around">
                          <v-col>
                            <div>{{x.instructor}} ({{x.crn}})</div>
                          </v-col>
                          <v-col cols="1">
                            <!-- Select/Unselect course (will add and drop to schedule) -->
                            <b-form-checkbox-group
                              size="sm"
                              style="align: right"
                              :id="x.crn"
                              v-model="schedule"
                              :options="[{text: '', value: x}]"
                              @change="onCheckbox"
                            ></b-form-checkbox-group>
                          </v-col>
                        </v-row>
                        <v-row justify="space-around">
                          <v-col>
                            <v-icon v-if="x.days.sunday" small :color="x.class_color">fas fa-square</v-icon>
                            <v-icon v-if="!x.days.sunday" small>far fa-square</v-icon>
                            <v-icon v-if="x.days.monday" small :color="x.class_color">fas fa-square</v-icon>
                            <v-icon v-if="!x.days.monday" small>far fa-square</v-icon>
                            <v-icon v-if="x.days.tuesday" small :color="x.class_color">fas fa-square</v-icon>
                            <v-icon v-if="!x.days.tuesday" small>far fa-square</v-icon>
                            <v-icon
                              v-if="x.days.wednesday"
                              small
                              :color="x.class_color"
                            >fas fa-square</v-icon>
                            <v-icon v-if="!x.days.wednesday" small>far fa-square</v-icon>
                            <v-icon
                              v-if="x.days.thursday"
                              small
                              :color="x.class_color"
                            >fas fa-square</v-icon>
                            <v-icon v-if="!x.days.thursday" small>far fa-square</v-icon>
                            <v-icon v-if="x.days.friday" small :color="x.class_color">fas fa-square</v-icon>
                            <v-icon v-if="!x.days.friday" small>far fa-square</v-icon>
                            <v-icon
                              v-if="x.days.saturday"
                              small
                              :color="x.class_color"
                            >fas fa-square</v-icon>
                            <v-icon v-if="!x.days.saturday" small>far fa-square</v-icon>
                          </v-col>
                          <v-col>
                            <div>{{x.schedule_type}}: {{x.times.start.substring(11,16)}} - {{x.times.end.substring(11,16)}}</div>
                          </v-col>
                          <v-col cols="1">
                            <v-icon :color="x.campus_color" :id="x.crn + 'tooltip'">fas fa-school</v-icon>
                            <b-tooltip placement="bottom" :target="x.crn + 'tooltip'" triggers="hover">
                              <span>{{x.campus}}: {{x.location}}</span>
                            </b-tooltip>

                          </v-col>
                        </v-row>
                      </v-container>
                    </v-list-item-content>
                  </v-list-item>
                </v-card>
              </v-expansion-panel-content>
              <!-- Remove selected course title -->
              <v-expansion-panel-content class="text-center" :id="title">
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteSelectedTitle(title)"
                >Delete</button>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
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
      schedule_id: '',
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
          this.schedule_id = res.data.id;
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
          .post(path, {
            classTitle,
            goal: 'getSections',
            subject: this.subject,
          })
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
      const path = `http://localhost:5000/builder/${this.schedule_id}`;
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
      const path = `http://localhost:5000/builder/${this.schedule_id}`;
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
