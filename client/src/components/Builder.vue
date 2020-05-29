<template>
  <div style="max-height: 100%">
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="/">MC Scheduler</b-navbar-brand>
      <v-spacer></v-spacer>
      <span style="color: white; align: center">{{name}}</span>
      <v-spacer></v-spacer>
      <v-btn @click="onCreateSchedule()">Create New Schedule</v-btn>
      <v-select
        style="background-color: white; width: 20%"
        label="name"
        :options="schedules"
        @input="getScheduleBuilder"
        placeholder="Select an existing schedule"
      ></v-select>
    </b-navbar>
    <v-container>
      <v-row>
        <!-- LHS of screen (calendar) -->
        <v-col cols="8" style="overflow: scroll; max-height: 750px">
          <v-sheet>
            <v-calendar
              interval-height="50"
              first-interval="8"
              interval-count="13"
              ref="calendar"
              :value="today"
              :events="events"
              color="primary"
              type="week"
              :event-color="getEventColor"
            ></v-calendar>
          </v-sheet>
          <p style="text-align: right">Credits: {{parseFloat(credits)}}</p>
        </v-col>

        <!-- RHS of screen -->
        <v-col cols="4" style="overflow: scroll; max-height: 750px">
          <!-- Select Subject -->
          <v-select :options="subjects" @input="getClassTitles" placeholder="Select a subject" />
          <!-- Select course title -->
          <v-select
            v-if="class_titles.length"
            :options="class_titles"
            @input="getClassSections"
            label="title"
            placeholder="Select a course"
          />

          <!-- Select section -->
          <v-expansion-panels>
            <v-expansion-panel v-for="(sections, title) in selected_titles" :key="title">
              <!-- Collapse button (title) -->
              <v-expansion-panel-header outline :color="sections[0].class_color">
                {{title}}
                <template v-slot:actions>
                  <v-icon color="white">mdi-check</v-icon>
                </template>
              </v-expansion-panel-header>
              <v-expansion-panel-content :id="title" v-for="(x, index) in sections" :key="index">
                <!-- Card containing class information -->
                <v-card
                  class="mx-auto"
                  outlined
                  v-on:mouseover="mouseOver(x)"
                  v-on:mouseleave="mouseLeave(x)"
                >
                  <v-list style="padding-top: 0px; padding-bottom: 5px; overflow-x: auto">
                    <v-list-item dense>
                      <v-list-item-content style="overflow-x: auto">
                        <div>
                          <v-container fluid style="height: 50px; width: 400px; padding-top: 0px">
                            <v-row justify="space-around" style="height: 22px">
                              <v-col cols="1">
                                <v-icon
                                  :color="x.campus_color"
                                  :id="x.crn + 'tooltip'"
                                >fas fa-school</v-icon>
                                <b-tooltip
                                  :target="x.crn + 'tooltip'"
                                  triggers="hover"
                                >
                                  <span>{{x.campus}}: {{x.location}}</span>
                                </b-tooltip>
                              </v-col>
                              <v-col>
                                <div style="text-align: left">{{x.instructor}} ({{x.crn}})</div>
                              </v-col>
                            </v-row>
                            <!-- Color coded boxes -->
                            <v-row justify="space-around">
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
                              <v-col cols="4" style="padding-top: 18px">
                                <v-icon
                                  v-if="x.days.sunday"
                                  small
                                  :color="x.class_color"
                                >fas fa-square</v-icon>
                                <v-icon v-if="!x.days.sunday" small>far fa-square</v-icon>
                                <v-icon
                                  v-if="x.days.monday"
                                  small
                                  :color="x.class_color"
                                >fas fa-square</v-icon>
                                <v-icon v-if="!x.days.monday" small>far fa-square</v-icon>
                                <v-icon
                                  v-if="x.days.tuesday"
                                  small
                                  :color="x.class_color"
                                >fas fa-square</v-icon>
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
                                <v-icon
                                  v-if="x.days.friday"
                                  small
                                  :color="x.class_color"
                                >fas fa-square</v-icon>
                                <v-icon v-if="!x.days.friday" small>far fa-square</v-icon>
                                <v-icon
                                  v-if="x.days.saturday"
                                  small
                                  :color="x.class_color"
                                >fas fa-square</v-icon>
                                <v-icon v-if="!x.days.saturday" small>far fa-square</v-icon>
                              </v-col>
                              <v-col style="padding-top: 18px">
                                <div v-if="!x.times.tba" style="text-align: left">
                                  {{x.schedule_type}}:
                                  {{x.times.start.substring(11,16)}}
                                  - {{x.times.end.substring(11,16)}}
                                </div>
                                <div v-if="x.times.tba">{{x.schedule_type}}: TBA</div>
                              </v-col>
                            </v-row>
                          </v-container>
                        </div>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-expansion-panel-content>
              <!-- Remove selected course title -->
              <v-expansion-panel-content :id="title">
                <v-container style="height: 50px; padding-top: 0px; padding-bottom: 0px">
                  <v-row>
                    <v-col class="text-left">
                      <span>Credits: {{sections[0].credits}}</span>
                    </v-col>
                    <v-col class="text-right">
                      <v-btn
                        class="mx-2"
                        fab
                        dark
                        small
                        color="red"
                        @click="onDeleteSelectedTitle(title)"
                      >
                        <v-icon dark>far fa-trash-alt</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-col>
      </v-row>
    </v-container>
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
      credits: 0,

      today: '1899-12-31',
      events: [],
      hover_bool: false,
      schedules: [],
    };
  },
  methods: {
    // Refresh all data with schedule file
    getSchedule() {
      if (this.schedule_id) {
        const path = `http://localhost:5000/builder/${this.schedule_id}`;
        axios
          .get(path)
          .then((res) => {
            this.schedule = res.data.schedule;
            this.name = res.data.name;
            this.schedule_id = res.data.id;
            this.subjects = res.data.subjects;
            this.selected_titles = res.data.selected_titles;
            const tempClasses = [];
            this.credits = 0.0;
            this.schedule.forEach((element) => {
              this.credits += parseFloat(element.credits);
              element.times.meetings.forEach((e) => {
                tempClasses.unshift({
                  name: element.course,
                  start: e.start,
                  end: e.end,
                  color: element.class_color,
                  crn: element.crn,
                });
              });
            });
            this.events = tempClasses;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            this.getSchedule();
          });
      } else {
        // this.$router.push({ name: '' });
      }
    },
    // Gets titles for select dropdown
    getClassTitles(subject) {
      const path = `http://localhost:5000/builder/${this.schedule_id}`;
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
          this.getSchedule();
        });
    },
    // Gets classes for corrisponding title (used in expansion cards)
    getClassSections(classTitle) {
      if (classTitle != null) {
        const path = `http://localhost:5000/builder/${this.schedule_id}`;
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
            this.getSchedule();
          });
      }
    },
    // When checkbox is clicked
    onCheckbox(update) {
      this.updateSchedule(update);
    },
    // Add or drop class
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
    // When delete button is clicked
    onDeleteSelectedTitle(selectedTitle) {
      this.removeSelectedTitle(selectedTitle);
    },
    // Removes all instances of selected title from schedule
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
    getEventColor(event) {
      return event.color;
    },
    // Mouse hover over section adds suggested (gray) event
    mouseOver(course) {
      let alreadyAdded = false;
      this.schedule.forEach((c) => {
        if (c.crn === course.crn) alreadyAdded = true;
      });
      if (!this.hover_bool && !alreadyAdded) {
        course.times.meetings.forEach((e) => {
          this.events.push({
            name: course.course,
            start: e.start,
            end: e.end,
            color: '#A0A0A0',
            crn: course.crn,
          });
        });
        this.hover_bool = true;
      }
    },
    // Mouse hover leaves, removes suggested (gray) event
    mouseLeave(course) {
      let alreadyAdded = false;
      this.schedule.forEach((c) => {
        if (c.crn === course.crn) alreadyAdded = true;
      });
      if (this.hover_bool && !alreadyAdded) {
        this.events = this.events.filter(x => x.crn !== course.crn);
        this.hover_bool = false;
      }
    },
    getSchedules() {
      const path = 'http://localhost:5000/schedules';
      axios
        .get(path)
        .then((res) => {
          this.schedules = res.data.schedules;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getScheduleBuilder(schedule) {
      this.schedule_id = schedule.id;
      this.$router.push({ path: `/builder/${this.schedule_id}` });
      this.getSchedule();
    },
    onCreateSchedule() {
      this.createSchedule();
    },
    createSchedule() {
      const path = 'http://localhost:5000/create';
      axios
        .get(path)
        .then((res) => {
          this.getSchedules();
          this.getScheduleBuilder(res.data.schedule_file);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  mounted() {
    this.$refs.calendar.scrollToTime('8:00');
  },
  created() {
    this.schedule_id = this.$route.params.id;
    this.getSchedule();
    this.getSchedules();
  },
};
</script>

<style>
.my-event {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  border-radius: 2px;
  background-color: #1867c0;
  color: #ffffff;
  border: 1px solid #1867c0;
  font-size: 12px;
  padding: 3px;
  cursor: pointer;
  margin-bottom: 1px;
  left: 4px;
  margin-right: 8px;
  position: relative;
}

.my-event.with-time {
  position: absolute;
  right: 4px;
  margin-right: 0px;
}

.v-calendar-daily_head-day-label {
  display: none;
}

.right-col {
  overflow-y: scroll;
  height: 100%;
}
</style>
