import { ApifyClient } from 'apify-client';
import { initializeApp, cert } from 'firebase-admin/app';
import { getDatabase } from 'firebase-admin/database';
import serviceAccount from '/Users/ashnakhetan/Desktop/Import/lost-2317d-firebase-adminsdk-8s3gl-deef4eb57f.json' assert { type: 'json' };

// Initialize the ApifyClient with API token
const client = new ApifyClient({
    token: 'apify_api_Bb1VcyB0ZqyqjMXhCyM6dykOJkz2Hd3Hj7fo',
});

// (async () => {
//     // Run the Actor and wait for it to finish
//     const run = await client.actor("if12dqi9gDL3GUpcq").call(input({attraction: "bayfront park", location: "miami"}));

//     // Fetch and print Actor results from the run's dataset (if any)
//     console.log('Results from dataset');
//     const { items } = await client.dataset(run.defaultDatasetId).listItems();
//     items.forEach((item) => {
//         console.dir(item);
//     });
// })();

const runActorAndGetUrls = async (attraction, location) => {

    const input = ({attraction, location}) => {
        return {
            "search": [attraction, location],
            "startUrls": [
                // "https://www.tiktok.com/search?q=music&t=1670685477846",
                // "https://www.tiktok.com/search?q=dance&t=1670685484412",
                // "https://www.tiktok.com/search?q=challenge&t=1670685494590"
            ],
            "maxItems": 3,
            "endPage": 1,
            "extendOutputFunction": ($) => { return {} },
            "customMapFunction": (object) => { return {...object} },
            "proxy": {
                "useApifyProxy": true
        }
    }};
  
    const run = await client.actor("if12dqi9gDL3GUpcq").call(input({attraction: attraction, location: location}));

    console.log('Results from dataset');
    const { items } = await client.dataset(run.defaultDatasetId).listItems();
    // items.forEach((item) => {
    //     console.dir(item);
    // });
    const embedObj = {
        url: items[0].url
    }
    console.log(embedObj);

    return embedObj;
};

const connectDb = () => {
    
    // const serviceAccount = require('/Users/ashnakhetan/Desktop/Import/lost-2317d-firebase-adminsdk-8s3gl-deef4eb57f.json');

    initializeApp({
    credential: cert(serviceAccount),
    databaseURL: 'https://lost-2317d-default-rtdb.firebaseio.com/'
    });
  
    const db = getDatabase();
    return db;
}

const updateFirebase = async () => {
    const db = connectDb()
    const destinationsRef = db.ref('Destinations');
    destinationsRef.once('value', async (snapshot) => {
        const destinations = snapshot.val();
        for (let location in destinations) {
        for (let attraction in destinations[location]) {
            const attractionData = destinations[location][attraction];
            // Example function to run the Apify actor and get TikTok URLs
            const tikTokUrls = await runActorAndGetUrls(attraction, location);

            // Update the Realtime Database with TikTok URLs
            const updateRef = destinationsRef.child(`${location}/${attraction}`);
            updateRef.update({
                tikTokUrl: tikTokUrls.url,
            });
        }
        }
    });
  };
  
  updateFirebase().then(() => console.log('Update complete'));