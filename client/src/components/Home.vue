<template>
  <div>
    <!-- Header -->
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="/">MC Scheduler</b-navbar-brand>
    </b-navbar>
    <br />
    <br />
    <v-container fluid style="min-height: 100%; height: 100%">
      <v-row>
        <v-col cols="7">
          <div>
            <b-carousel
              id="carousel-1"
              v-model="slide"
              :interval="4000"
              controls
              indicators
              background="white"
              img-width="1024"
              img-height="480"
              style="text-shadow: 1px 1px 2px #333;"
              @sliding-start="onSlideStart"
              @sliding-end="onSlideEnd"
            >
              <!-- Slides with image only -->
              <b-carousel-slide img-src="https://i.gyazo.com/a7c8c8565f2f610e7c4fdd580ddb1f58.png"></b-carousel-slide>

              <!-- Text slides with image -->
              <b-carousel-slide
                img-src="https://i.gyazo.com/c427ca53d0fbb9549a54bda0e0a5d704.png"
              ><h1 stlye="color: black">Suggestive Highlighting</h1></b-carousel-slide>

            </b-carousel>
          </div>
        </v-col>
        <v-col>
          <b-jumbotron>
            <template v-slot:header>MC Scheduler</template>

            <template v-slot:lead>
              Plan your semester schedule easily with MC Scheduler.
            </template>

            <hr class="my-4" />

            <p>
              Create a new schedule or choose an existing schedule to start!
            </p>
            <v-container fluid>
              <v-row>
                <v-col>
                  <v-btn @click="onCreateSchedule()">Create New Schedule</v-btn>
                </v-col>
                <v-col>
                  <v-select
                    style="background-color: white"
                    label="name"
                    :options="schedules"
                    @input="getScheduleBuilder"
                    placeholder="Select an existing schedule"
                  ></v-select>
                </v-col>
              </v-row>
            </v-container>
          </b-jumbotron>
        </v-col>
      </v-row>
    </v-container>
    <!-- <v-footer dark padless default style="relative"> -->
    <v-footer dark padless absolute>
      <v-card class="flex" flat tile>
        <v-card-title class="teal">
          <strong class="subheading">Get connected with us on social networks!</strong>

          <v-spacer></v-spacer>

          <v-btn v-for="icon in icons" :key="icon" class="mx-4" dark icon :href="icon.url">
            <v-icon size="24px">{{ icon.icon }}</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="py-2 white--text text-center">
          {{ new Date().getFullYear() }} —
          <strong>MC Scheduler</strong>
        </v-card-text>
      </v-card>
    </v-footer>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      slide: 0,
      sliding: null,
      icons: [
        {
          icon: 'fab fa-github',
          url: 'https://github.com/jojo20872/MC-Schedule-Builder',
        },
        {
          icon: 'fab fa-linkedin',
          url: 'https://www.linkedin.com/in/jschne/',
        },
      ],
      schedules: [],
    };
  },
  methods: {
    onSlideStart() {
      this.sliding = true;
    },
    onSlideEnd() {
      this.sliding = false;
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
    getScheduleBuilder(schedule) {
      const { id } = schedule;
      this.$router.push({ path: `/builder/${id}` });
    },
  },
  created() {
    this.getSchedules();
  },
};
</script>

<style>
html,
body {
  height: 100%;
}
</style>
