<template >
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="/">MC-Scheduler</b-navbar-brand>
    </b-navbar>
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
              background="#ababab"
              img-width="1024"
              img-height="480"
              style="text-shadow: 1px 1px 2px #333;"
              @sliding-start="onSlideStart"
              @sliding-end="onSlideEnd"
            >
              <!-- Text slides with image -->
              <b-carousel-slide
                caption="First slide"
                text="Nulla vitae elit libero, a pharetra augue mollis interdum."
                img-src="https://picsum.photos/1024/480/?image=52"
              ></b-carousel-slide>

              <!-- Slides with custom text -->
              <b-carousel-slide img-src="https://picsum.photos/1024/480/?image=54">
                <h1>Hello world!</h1>
              </b-carousel-slide>

              <!-- Slides with image only -->
              <b-carousel-slide img-src="https://i.gyazo.com/a7c8c8565f2f610e7c4fdd580ddb1f58.png"></b-carousel-slide>
            </b-carousel>
          </div>
        </v-col>
        <v-col>
          <b-jumbotron>
            <template v-slot:header>MC Scheduler</template>

            <template v-slot:lead>
              This is a simple hero unit, a simple jumbotron-style component for calling extra attention to
              featured content or information.
            </template>

            <hr class="my-4" />

            <p>
              It uses utility classes for typography and spacing to space content out within the larger
              container.
            </p>

            <v-btn large @click="onCreateSchedule()">Create New Schedule</v-btn>
            <p>Select from existing schedules:</p>
            <v-select
              style="background-color: white"
              label="name"
              :options="schedules"
              @input="getScheduleBuilder"
            ></v-select>
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
      // const path = 'http://localhost:5000/builder';
      // axios
      //   .get(path)
      //   .then((res) => {
      //     this.schedules = res.data.schedules;
      //   })
      //   .catch((error) => {
      //     // eslint-disable-next-line
      //     console.error(error);
      //     this.getSchedules();
      //   });
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
