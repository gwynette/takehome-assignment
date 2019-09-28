<template>
  <!-- PART 4: Add your code here -->
  <div>
    <!--Part 4: Displayed show names-->
    <p>{{  name  }}</p>
    <!--Part 4: Rendered a Counter component and passed prop "episodes_seen" as initial count-->
    <Counter v-bind:count="episodes_seen"></Counter>
    <p></p>
  </div>
</template>

<script>
// PART 4: Add your code here
import Counter from "./Counter.vue";
export default {
  components:{
    Counter
  },
// Part 4: Added properties id, name, episodes_seen
  props:{
    id:{

    },
    name:{

    },
    episodes_seen:{

    }
  }
};
</script>

<style>
</style>
