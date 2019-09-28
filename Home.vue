<template>
  <div>
    <!-- PART 1: Pass in a "complete" prop here -->
    <Instructions complete/>

    <!--BONUS: Add input and submit button for new show (Attempted but did not finish)
    <input v-model="newShowName" placeholder="Add New Show">
    <button v-on:click="shows.push(newShow())">Submit</button>
    <p></p>
    -->

    <!-- PART 4: Modify the Show component to accept all of these props -->
    <!--Name, id, episodes_seen defined in Home is bound to the props in Show-->
    <Show
      v-for="show in shows"
      :key="show.id"
      :id="show.id"
      :name="show.name"
      :episodes_seen="show.episodes_seen"
    />
  </div>
</template>


<script>
import Instructions from "./Instructions.vue";
import Show from "./Show.vue";

export default {
  components: {
    Instructions,
    Show
  },
  // Part of attempted BONUS task
  /*
  props:{
    newShowName:{

    }
  },
  methods:{
    newId(){
      return (length(shows) + 1)
    },
    newShow(){
      newshowId = newId();
      newName = newShowName;
      return { id: newshowId, name: newName, episodes_seen: 0}
    }
  },
  */
  data() {
    return {
      shows: [
        { id: 1, name: "Game of Thrones", episodes_seen: 0 },
        { id: 2, name: "Naruto", episodes_seen: 220 },
        { id: 3, name: "Black Mirror", episodes_seen: 3 }
      ]
    };
  }
};
</script>

<style>
</style>


