import api from '@api';


// Submissions by round
export const SET_CURRENT_SUBMISSION_ROUND = 'SET_CURRENT_SUBMISSION_ROUND';
export const SET_CURRENT_SUBMISSION = 'SET_CURRENT_SUBMISSION';
export const UPDATE_SUBMISSIONS_BY_ROUND = 'UPDATE_SUBMISSIONS_BY_ROUND';
export const START_LOADING_SUBMISSIONS_BY_ROUND = 'START_LOADING_SUBMISSIONS_BY_ROUND';
export const FAIL_LOADING_SUBMISSIONS_BY_ROUND = 'FAIL_LOADING_SUBMISSIONS_BY_ROUND';


export const setCurrentSubmissionRound = id => ({
    type: SET_CURRENT_SUBMISSION_ROUND,
    id,
});

export const setCurrentSubmission = id => ({
    type: SET_CURRENT_SUBMISSION,
    id,
});

export const fetchSubmissionsByRound = roundId => {
    return async function(dispatch) {
        dispatch(startLoadingSubmissionsByRound());
        try {
            const response = await api.fetchSubmissionsByRound(roundId);
            const json = await response.json();
            if (!response.ok) {
                dispatch(failLoadingSubmissionsByRound());
                return;
            }
            dispatch(updateSubmissionsByRound(roundId, json));
        } catch (e) {
            console.error(e);
            dispatch(failLoadingSubmissionsByRound());
        }
    };
};


const updateSubmissionsByRound = (roundId, data) => ({
    type: UPDATE_SUBMISSIONS_BY_ROUND,
    roundId,
    data,
});


const startLoadingSubmissionsByRound = () => ({
    type: START_LOADING_SUBMISSIONS_BY_ROUND,
});



const failLoadingSubmissionsByRound = () => ({
    type: FAIL_LOADING_SUBMISSIONS_BY_ROUND,
});