<template>
  <div>
    <!-- Header -->
    <b-navbar toggleable="lg" type="dark" variant="info" fixed="top">
      <b-navbar-brand href="#">MC Scheduler: {{name}}</b-navbar-brand>
    </b-navbar>
    <v-container>
      <v-app id="inspire">
        <v-row>
          <!-- LHS of screen (calendar) -->
          <v-col>
            <v-sheet>
              <v-calendar
                interval-height="36"
                first-interval="6"
                interval-count="16"
                ref="calendar"
                :value="today"
                :events="events"
                color="primary"
                type="week"
                :event-color="getEventColor"
                style="height: 100%"
              ></v-calendar>
            </v-sheet>
          </v-col>

          <!-- RHS of screen -->
          <v-col cols="4" style="max-height: 50%" class="overflow-y-auto">
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
                  <!-- Collapse button (title) -->
                  <v-expansion-panel-header outline :color="sections[0].class_color">
                    {{title}}
                    <template v-slot:actions>
                      <v-icon color="white">mdi-check</v-icon>
                    </template>
                  </v-expansion-panel-header>
                  <v-expansion-panel-content
                    :id="title"
                    v-for="(x, index) in sections"
                    :key="index"
                  >
                    <!-- Card containing class information -->
                    <v-card
                      class="mx-auto"
                      outlined
                      v-on:mouseover="mouseOver(x)"
                      v-on:mouseleave="mouseLeave"
                    >
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
                              <v-col>
                                <div v-if="!x.times.tba">
                                  {{x.schedule_type}}:
                                  {{x.times.start.substring(11,16)}}
                                  - {{x.times.end.substring(11,16)}}
                                </div>
                                <div v-if="x.times.tba">{{x.schedule_type}}: TBA</div>
                              </v-col>
                              <v-col cols="1">
                                <v-icon
                                  :color="x.campus_color"
                                  :id="x.crn + 'tooltip'"
                                >fas fa-school</v-icon>
                                <b-tooltip
                                  placement="bottom"
                                  :target="x.crn + 'tooltip'"
                                  triggers="hover"
                                >
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
          </v-col>
        </v-row>
      </v-app>
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

      today: '1899-12-31',
      events: [],
      hover_bool: false,
      hover_count: 0,
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
          const tempClasses = [];
          this.schedule.forEach((element) => {
            element.times.meetings.forEach((e) => {
              tempClasses.push({
                name: element.course,
                start: e.start,
                end: e.end,
                color: element.class_color,
              });
            });
          });
          this.events = tempClasses;
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
    getEventColor(event) {
      return event.color;
    },
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
          });
          this.hover_count += 1;
        });
        this.hover_bool = true;
      }
    },
    mouseLeave() {
      let i;
      for (i = 0; i < this.hover_count; i += 1) {
        this.events.pop();
      }
      this.hover_bool = false;
      this.hover_count = 0;
    },
  },
  mounted() {
    this.$refs.calendar.scrollToTime('8:00');
  },
  created() {
    this.getSchedule();
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
</style>
